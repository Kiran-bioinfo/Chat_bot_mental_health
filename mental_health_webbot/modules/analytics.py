import sqlite3
import numpy as np
from datetime import datetime, timedelta
import logging
from typing import dict, list
import json

logger = logging.getLogger(__name__)

class MoodAnalytics:
    """Analyze mood trends, detect patterns, and provide insights."""
    
    CRISIS_KEYWORDS = {
        'suicide': ['suicide', 'suicidal', 'kill myself', 'end it all', 'don\'t want to live'],
        'self_harm': ['self harm', 'hurt myself', 'cut myself', 'injure'],
        'hopelessness': ['hopeless', 'worthless', 'no point', 'give up', 'pointless'],
        'severe_depression': ['severely depressed', 'completely numb', 'can\'t go on']
    }
    
    def __init__(self, db_path: str = 'mental_health_webbot/data/user_data.db'):
        self.db_path = db_path
        self.create_tables()
    
    def create_tables(self) -> None:
        """Create database tables for mood tracking."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Mood log table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS mood_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    mood_score INTEGER,
                    mood_label TEXT,
                    emotions TEXT,
                    triggers TEXT,
                    intensity_level TEXT,
                    notes TEXT,
                    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Conversation logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversation_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    user_message TEXT,
                    bot_response TEXT,
                    sentiment TEXT,
                    crisis_detected BOOLEAN,
                    response_quality REAL,
                    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Crisis alerts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS crisis_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    crisis_type TEXT,
                    severity_score REAL,
                    content TEXT,
                    alert_sent BOOLEAN,
                    alert_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Analytics tables created successfully")
        
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
    
    def log_mood(self, user_id: str, mood_score: int, mood_label: str, 
                 emotions: list = None, triggers: list = None, 
                 intensity_level: str = None, notes: str = None) -> bool:
        """Log user mood entry."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO mood_logs 
                (user_id, mood_score, mood_label, emotions, triggers, intensity_level, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                mood_score,
                mood_label,
                json.dumps(emotions or []),
                json.dumps(triggers or []),
                intensity_level,
                notes
            ))
            
            conn.commit()
            conn.close()
            logger.info(f"Logged mood for user {user_id}: {mood_label}")
            return True
        
        except Exception as e:
            logger.error(f"Error logging mood: {e}")
            return False
    
    def log_conversation(self, user_id: str, user_message: str, bot_response: str,
                        sentiment: str = None, crisis_detected: bool = False,
                        response_quality: float = None) -> bool:
        """Log conversation exchange."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO conversation_logs
                (user_id, user_message, bot_response, sentiment, crisis_detected, response_quality)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                user_message,
                bot_response,
                sentiment,
                crisis_detected,
                response_quality
            ))
            
            conn.commit()
            conn.close()
            return True
        
        except Exception as e:
            logger.error(f"Error logging conversation: {e}")
            return False
    
    def detect_crisis(self, text: str) -> dict:
        """Detect crisis indicators in text."""
        text_lower = text.lower()
        detected_crises = []
        severity_score = 0.0
        
        for crisis_type, keywords in self.CRISIS_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    detected_crises.append(crisis_type)
                    severity_score += 0.25
                    break
        
        # Remove duplicates
        detected_crises = list(set(detected_crises))
        
        # Check for multiple crisis indicators (increases severity)
        if len(detected_crises) > 1:
            severity_score += 0.2
        
        # Cap severity at 1.0
        severity_score = min(1.0, severity_score)
        
        return {
            'is_crisis': len(detected_crises) > 0,
            'crisis_types': detected_crises,
            'severity_score': round(severity_score, 2),
            'requires_immediate_help': severity_score > 0.7
        }
    
    def log_crisis_alert(self, user_id: str, crisis_type: str, severity_score: float, 
                        content: str, alert_sent: bool = False) -> bool:
        """Log crisis alert."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO crisis_alerts
                (user_id, crisis_type, severity_score, content, alert_sent)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, crisis_type, severity_score, content, alert_sent))
            
            conn.commit()
            conn.close()
            logger.warning(f"Crisis alert logged for user {user_id}: {crisis_type}")
            return True
        
        except Exception as e:
            logger.error(f"Error logging crisis alert: {e}")
            return False
    
    def get_mood_trends(self, user_id: str, days: int = 7) -> dict:
        """Get mood trends for a user over specified days."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            cursor.execute('''
                SELECT mood_score, mood_label, logged_at FROM mood_logs
                WHERE user_id = ? AND logged_at > ?
                ORDER BY logged_at ASC
            ''', (user_id, cutoff_date))
            
            moods = cursor.fetchall()
            conn.close()
            
            if not moods:
                return {
                    'user_id': user_id,
                    'period_days': days,
                    'total_entries': 0,
                    'data': []
                }
            
            scores = [m[0] for m in moods]
            labels = [m[1] for m in moods]
            dates = [m[2] for m in moods]
            
            trend = {
                'user_id': user_id,
                'period_days': days,
                'total_entries': len(moods),
                'average_mood': round(np.mean(scores), 2),
                'mood_range': {'min': min(scores), 'max': max(scores)},
                'trend': self._calculate_trend(scores),
                'data': [{
                    'score': score,
                    'label': label,
                    'date': date
                } for score, label, date in zip(scores, labels, dates)]
            }
            
            return trend
        
        except Exception as e:
            logger.error(f"Error getting mood trends: {e}")
            return {}
    
    def _calculate_trend(self, scores: list) -> str:
        """Calculate trend direction (improving/declining/stable)."""
        if len(scores) < 2:
            return 'insufficient_data'
        
        first_half_avg = np.mean(scores[:len(scores)//2])
        second_half_avg = np.mean(scores[len(scores)//2:])
        
        difference = second_half_avg - first_half_avg
        
        if difference > 0.5:
            return 'improving'
        elif difference < -0.5:
            return 'declining'
        else:
            return 'stable'
    
    def get_crisis_summary(self, user_id: str, days: int = 30) -> dict:
        """Get crisis summary for a user."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            cursor.execute('''
                SELECT crisis_type, severity_score, alert_time FROM crisis_alerts
                WHERE user_id = ? AND alert_time > ?
                ORDER BY alert_time DESC
            ''', (user_id, cutoff_date))
            
            alerts = cursor.fetchall()
            conn.close()
            
            summary = {
                'user_id': user_id,
                'period_days': days,
                'total_alerts': len(alerts),
                'high_severity_alerts': sum(1 for a in alerts if a[1] > 0.7),
                'crisis_types': list(set([a[0] for a in alerts])),
                'recent_alerts': [{
                    'type': a[0],
                    'severity': a[1],
                    'time': a[2]
                } for a in alerts[:5]]
            }
            
            return summary
        
        except Exception as e:
            logger.error(f"Error getting crisis summary: {e}")
            return {}
    
    def get_wellness_recommendations(self, user_id: str) -> list:
        """Generate wellness recommendations based on mood patterns."""
        try:
            trends = self.get_mood_trends(user_id, days=7)
            
            recommendations = []
            
            if not trends.get('data'):
                return ["Start tracking your mood to get personalized recommendations"]
            
            avg_mood = trends.get('average_mood', 5)
            trend_direction = trends.get('trend', 'stable')
            
            # Generate recommendations based on mood
            if avg_mood < 3:
                recommendations.extend([
                    "Consider reaching out to friends or family for support",
                    "Try a short meditation or breathing exercise (5-10 minutes)",
                    "Go for a walk outside - fresh air can help mood"
                ])
            elif avg_mood < 5:
                recommendations.extend([
                    "Practice mindfulness or journaling about your feelings",
                    "Engage in an activity you enjoy",
                    "Ensure you're getting enough sleep (7-9 hours)"
                ])
            else:
                recommendations.extend([
                    "Keep up the positive momentum with regular exercise",
                    "Share your positive experiences with others",
                    "Set small achievable goals to maintain momentum"
                ])
            
            # Add trend-specific recommendations
            if trend_direction == 'declining':
                recommendations.insert(0, "Your mood has been declining - consider talking to a professional")
            elif trend_direction == 'improving':
                recommendations.insert(0, "Your mood is improving - keep up these positive habits!")
            
            return recommendations
        
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return []


if __name__ == "__main__":
    analytics = MoodAnalytics()
    
    # Test mood logging
    print("Testing mood logging...")
    analytics.log_mood('user123', 7, 'happy', emotions=['joy', 'contentment'], triggers=['exercise'])
    
    # Test crisis detection
    print("\nTesting crisis detection...")
    crisis_texts = [
        "I'm feeling a bit down today",
        "I want to end it all",
        "I can't stop thinking about hurting myself"
    ]
    
    for text in crisis_texts:
        crisis = analytics.detect_crisis(text)
        print(f"Text: {text}")
        print(f"Crisis detected: {crisis['is_crisis']}, Severity: {crisis['severity_score']}")
        print()
