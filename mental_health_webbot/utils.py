import json
import random
import nltk
from nltk.stem import WordNetLemmatizer
import spacy
import numpy as np
import os
nlp = spacy.load('en_core_web_md')

# Download necessary NLTK data (only needs to be run once)
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    # Tokenize the text
    words = nltk.word_tokenize(text)
    # Lemmatize and convert to lowercase
    words = [lemmatizer.lemmatize(word.lower()) for word in words]
    return words

def bag_of_words(sentence, words, show_details=True):
    # Preprocess the sentence
    sentence_words = preprocess_text(sentence)
    # Initialize bag with 0 for each word
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return np.array(bag)

def generate_creative_response(user_input):
    responses = [
        "That's an interesting thought. Tell me more about what's on your mind.",
        "I hear you. Sometimes just talking about it helps. What else would you like to share?",
        "It sounds like you're going through something. I'm here to listen without judgment.",
        "I appreciate you sharing that with me. How does that make you feel?",
        "Thank you for opening up. What do you think is the next step for you?",
        "I'm here to support you. What's one small thing you can do for yourself today?",
        "That's a valid feeling. Can you describe it a bit more for me?",
        "I'm listening. What's been on your mind lately?",
        "It takes courage to share that. What do you need most right now?",
        "I'm glad you're talking about this. What's one thing that brings you comfort?"
    ]

    # Simple keyword-based enhancements for creativity
    if "stress" in user_input.lower() or "anxious" in user_input.lower():
        responses.append("Stress can be tough. Have you tried any relaxation techniques lately?")
    if "sad" in user_input.lower() or "depressed" in user_input.lower():
        responses.append("It's okay to feel sad. Remember, even small steps forward are progress.")
    if "happy" in user_input.lower() or "good" in user_input.lower():
        responses.append("That's wonderful to hear! What's making you feel good today?")
    if "lonely" in user_input.lower() or "alone" in user_input.lower():
        responses.append("Feeling lonely is tough. Connecting with others, even virtually, can sometimes help.")

    return random.choice(responses)

def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error getting Gemini response: {e}")
        return "I'm sorry, I'm having trouble connecting right now. Please try again later."

def get_response(user_input):
    # Use creative response for all responses for a more conversational experience
    return generate_creative_response(user_input)