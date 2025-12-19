from transformers import pipeline
import logging
from typing import dict

logger = logging.getLogger(__name__)

class EmotionDetector:
    """Detect emotions and sentiment from text using HuggingFace transformers."""
    
    def __init__(self):
        """Initialize emotion detection models."""
        try:
            # Sentiment analysis (positive/negative)
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english"
            )
            
            # Zero-shot emotion classification
            self.emotion_pipeline = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli"
            )
            
            self.emotion_labels = [
                'happy', 'sad', 'anxious', 'angry', 'calm',
                'frustrated', 'hopeful', 'lonely', 'stressed', 'confused'
            ]
            
            logger.info("EmotionDetector initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing EmotionDetector: {e}")
            self.sentiment_pipeline = None
            self.emotion_pipeline = None
    
    def detect_sentiment(self, text: str) -> dict:
        """Detect sentiment (positive/negative) from text."""
        if not self.sentiment_pipeline:
            return {'error': 'Sentiment model not loaded'}
        
        try:
            result = self.sentiment_pipeline(text)[0]
            return {
                'label': result['label'].lower(),
                'score': round(result['score'], 3),
                'is_negative': result['label'] == 'NEGATIVE'
            }
        except Exception as e:
            logger.error(f"Error in sentiment detection: {e}")
            return {'error': str(e)}
    
    def detect_emotions(self, text: str, top_k: int = 3) -> dict:
        """Detect specific emotions from text."""
        if not self.emotion_pipeline:
            return {'error': 'Emotion model not loaded'}
        
        try:
            result = self.emotion_pipeline(
                text,
                self.emotion_labels,
                multi_class=True
            )
            
            # Top emotions with scores
            emotions = []
            for label, score in zip(result['labels'][:top_k], result['scores'][:top_k]):
                emotions.append({
                    'emotion': label,
                    'confidence': round(score, 3)
                })
            
            return {
                'detected_emotions': emotions,
                'primary_emotion': emotions[0]['emotion'] if emotions else None
            }
        except Exception as e:
            logger.error(f"Error in emotion detection: {e}")
            return {'error': str(e)}
    
    def get_emotion_intensity(self, text: str) -> dict:
        """Calculate emotional intensity based on keywords and sentiment."""
        intensity_keywords = {
            'extreme': ['absolutely', 'extremely', 'severely', 'completely'],
            'high': ['very', 'really', 'quite', 'deeply'],
            'moderate': ['somewhat', 'fairly', 'rather', 'relatively'],
            'mild': ['slightly', 'a bit', 'somewhat', 'little']
        }
        
        text_lower = text.lower()
        intensity_level = 'low'
        
        for level, keywords in intensity_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                intensity_level = level
                break
        
        # Combine with sentiment for overall intensity
        sentiment = self.detect_sentiment(text)
        is_negative = sentiment.get('is_negative', False)
        
        intensity_score = {
            'low': 0.2,
            'mild': 0.4,
            'moderate': 0.6,
            'high': 0.8,
            'extreme': 1.0
        }.get(intensity_level, 0.5)
        
        # Increase score if sentiment is negative
        if is_negative:
            intensity_score = min(1.0, intensity_score * 1.2)
        
        return {
            'intensity_level': intensity_level,
            'intensity_score': round(intensity_score, 2),
            'is_negative': is_negative
        }
    
    def analyze_mental_health_state(self, text: str) -> dict:
        """Comprehensive mental health state analysis."""
        try:
            sentiment = self.detect_sentiment(text)
            emotions = self.detect_emotions(text)
            intensity = self.get_emotion_intensity(text)
            
            # Determine if immediate help might be needed
            crisis_indicators = [
                'suicide', 'self-harm', 'kill myself', 'end it',
                'hurt myself', 'no point', 'give up'
            ]
            has_crisis_indicators = any(
                indicator in text.lower() for indicator in crisis_indicators
            )
            
            return {
                'sentiment': sentiment,
                'emotions': emotions,
                'intensity': intensity,
                'crisis_indicators': has_crisis_indicators,
                'needs_immediate_help': has_crisis_indicators,
                'overall_state': self._classify_overall_state(
                    sentiment, emotions, intensity
                )
            }
        except Exception as e:
            logger.error(f"Error in mental health analysis: {e}")
            return {'error': str(e)}
    
    def _classify_overall_state(self, sentiment: dict, emotions: dict, intensity: dict) -> str:
        """Classify overall mental health state."""
        is_negative = sentiment.get('is_negative', False)
        intensity_score = intensity.get('intensity_score', 0.5)
        
        if not is_negative and intensity_score < 0.4:
            return 'positive'
        elif not is_negative:
            return 'neutral_positive'
        elif intensity_score > 0.7:
            return 'concerning'
        else:
            return 'neutral_negative'


if __name__ == "__main__":
    detector = EmotionDetector()
    
    test_texts = [
        "I'm feeling very happy and excited about my future!",
        "I'm extremely anxious and can't stop worrying about everything.",
        "I feel completely hopeless and don't see any point to anything."
    ]
    
    for text in test_texts:
        print(f"\nText: {text}")
        analysis = detector.analyze_mental_health_state(text)
        print(f"Analysis: {analysis}")
