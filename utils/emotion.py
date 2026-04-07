# Sinamor 
# Sinamor: Adding crisis detection and response mapping.
# Sinamor: Mental health apps need a safety net, especially for student stress.
# Sinamor: Let's make sure our friends at GNDEC have the right help nearby.

import streamlit as st
from transformers import pipeline
import datetime

@st.cache_resource
def get_emotion_model():
    return pipeline("text-classification", 
                    model="j-hartmann/emotion-english-distilroberta-base", 
                    return_all_scores=True)

def analyze_emotion(text):
    if not text:
        return []
    pipe = get_emotion_model()
    results = pipe(text)
    return results[0]

def get_top_emotion(text):
    results = analyze_emotion(text)
    if not results:
        return "neutral", 0.0
    top = max(results, key=lambda x: x['score'])
    return top['label'], top['score']

def check_crisis(text):
    """
    Sinamor: Hardcoded keywords for crisis detection.
    In a real app, this would use a more robust classifier.
    """
    keywords = ["suicide", "kill myself", "end my life", "harm myself", "worthless", "dying", "won't wake up"]
    text_lower = text.lower()
    for word in keywords:
        if word in text_lower:
            return True
    return False

EMOTION_RESPONSES = {
    "joy": "I am so happy to hear that, {name}! Tera din vadiya lang reha lagda. Keep spreading that positivity! 😊",
    "sadness": "I'm here for you, {name}. It's okay to feel low sometimes. Ro laina chahida jekar mann bhari hai. Tell me more? 💙",
    "anger": "I hear you. Don't worry, gussey vich asi sab kive na kive feel karde haan. Leh dasso ki hoya? 😤",
    "fear": "Take a deep breath, {name}. You're not alone. Assi milke face karaange jo vi hai. 🫂",
    "disgust": "That sounds rough. Kade kade things don't feel right. Let's talk it out. 🤮",
    "surprise": "Oh wow! Utte thalle tan chalda hi rehnda hai life vich. Kya baat hai! 😲",
    "neutral": "Hmm, I see. Hor sunao, hor ki chal reha GNDEC vich? 🧘"
}

EMOTION_EMOJIS = {
    "joy": "😊", "sadness": "💙", "anger": "😤", "fear": "😨", "disgust": "🤢", "surprise": "😲", "neutral": "🧘"
}

EMOTION_COLORS = {
    "joy": "#FF9933", "sadness": "#4169E1", "anger": "#DC143C", 
    "fear": "#8B008B", "neutral": "#808080", "surprise": "#FFD700", 
    "disgust": "#006400"
}
