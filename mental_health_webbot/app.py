from flask import Flask, render_template, request, jsonify
import csv
from datetime import datetime
import os
from utils import get_response
from pdf_utils import extract_text_from_pdf

# Configure paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), 'book_data_hackathon')
ALL_PDF_TEXT = ""

app = Flask(__name__)

PRE_CHAT_QUESTIONS = [
    {
        "question": "How would you describe your overall mood today?",
        "options": ["Very happy", "Neutral", "A bit down", "Sad", "Anxious"]
    },
    {
        "question": "How would you rate your current stress level?",
        "options": [
            "No stress", "Mild stress", "Moderate stress",
            "High stress", "Overwhelmed"
        ]
    },
    {
        "question": "How well have you been sleeping lately?",
        "options": [
            "Very well", "Adequately", "Sometimes restless",
            "Often restless", "Rarely sleep well"
        ]
    },
    {
        "question": "How connected do you feel to others?",
        "options": [
            "Very connected", "Somewhat connected", "Neutral",
            "A bit isolated", "Very isolated"
        ]
    },
    {
        "question": "When faced with challenges, how effectively do you cope?",
        "options": [
            "Very effectively", "Mostly effectively", "Sometimes struggle",
            "Often struggle", "Rarely cope well"
        ]
    }
]

conversation_states = {}

@app.route('/')
def index():
    """Handle the index route and initialize session if needed."""
    try:
        # For simplicity, using a fixed session ID
        session_id = 'user123'
        if session_id not in conversation_states:
            conversation_states[session_id] = {
                'question_index': 0,
                'mood_answers': []
            }
        return render_template('index.html')
    except Exception as e:
        app.logger.error(f"Error in index route: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/get_initial_question', methods=['GET'])
def get_initial_question():
    """Get the initial or next question for the mood assessment."""
    try:
        session_id = 'user123'
        has_questions = len(PRE_CHAT_QUESTIONS)
        in_assessment = (
            session_id in conversation_states and
            conversation_states[session_id]['question_index'] < has_questions
        )
        
        if in_assessment:
            question_data = PRE_CHAT_QUESTIONS[
                conversation_states[session_id]['question_index']
            ]
            return jsonify({
                'question': question_data['question'],
                'options': question_data['options']
            })
        
        return jsonify({'question': 'Welcome back! How can I help you today?'})
    except Exception as e:
        app.logger.error(f"Error in get_initial_question route: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages and mood assessment responses."""
    try:
        user_message = request.json.get('message')
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        session_id = 'user123'
        if session_id not in conversation_states:
            conversation_states[session_id] = {
                'question_index': 0,
                'mood_answers': []
            }

        current_state = conversation_states[session_id]
        has_questions = len(PRE_CHAT_QUESTIONS)

        if current_state['question_index'] < has_questions:
            # During mood assessment phase
            current_state['mood_answers'].append(user_message)
            current_state['question_index'] += 1

            if current_state['question_index'] < has_questions:
                next_question_data = PRE_CHAT_QUESTIONS[
                    current_state['question_index']
                ]
                return jsonify({
                    'response': next_question_data['question'],
                    'options': next_question_data['options']
                })
            
            mood_summary = analyze_mood(current_state['mood_answers'])
            return jsonify({
                'response': f"{mood_summary}\nHow can I help you today?"
            })
        
        # Normal chat phase
        response = get_response(user_message)
        return jsonify({'response': response})

    except Exception as e:
        app.logger.error(f"Error in chat route: {e}")
        return jsonify({'error': 'Internal server error'}), 500

def analyze_mood(mood_answers):
    """Analyze the mood based on the answers provided."""
    try:
        # Simple mood analysis
        concern_level = 0
        positive_responses = [
            'Very happy', 'No stress', 'Very well',
            'Very connected', 'Very effectively'
        ]
        negative_responses = [
            'Sad', 'Anxious', 'High stress', 'Overwhelmed',
            'Rarely sleep well', 'Very isolated', 'Rarely cope well'
        ]
        
        for answer in mood_answers:
            if answer in negative_responses:
                concern_level += 1
            elif answer in positive_responses:
                concern_level -= 1
        
        if concern_level <= -3:
            return (
                "I'm glad to see you're doing well! "
                "Remember that it's okay to have good days."
            )
        elif concern_level >= 3:
            return (
                "I notice you might be going through a challenging time. "
                "Remember, it's okay to seek help when needed."
            )
        
        return (
            "Thank you for sharing how you're feeling. "
            "I'm here to listen and support you."
        )
            
    except Exception as e:
        app.logger.error(f"Error in mood analysis: {e}")
        return "Thank you for sharing your feelings with me."

@app.before_request
def load_pdf_data():
    """Load PDF data before processing any request."""
    global ALL_PDF_TEXT
    try:
        if not ALL_PDF_TEXT and os.path.exists(PDF_DATA_DIR):
            for root, _, files in os.walk(PDF_DATA_DIR):
                for file in files:
                    if file.endswith('.pdf'):
                        pdf_path = os.path.join(root, file)
                        try:
                            ALL_PDF_TEXT += extract_text_from_pdf(pdf_path)
                        except Exception as e:
                            app.logger.error(
                                f"Error loading PDF {pdf_path}: {e}"
                            )
    except Exception as e:
        app.logger.error(f"Error in load_pdf_data: {e}")

if __name__ == '__main__':
    app.run(debug=True)