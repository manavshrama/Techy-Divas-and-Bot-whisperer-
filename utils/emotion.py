# Sinamor
import streamlit as st
from transformers import pipeline

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
    return results[0] # returns list of dictionaries

def check_crisis(text):
    keywords = ["suicide", "kill myself", "end my life", "harm myself", "worthless", "dying", "won't wake up", "marna", "muat", "vadhna"]
    text_lower = text.lower()
    for word in keywords:
        if word in text_lower:
            return True
    return False

EMOTION_RESPONSES = {
    "joy": {
        "en": "I'm so glad you're feeling good, {name}! Keep up the positive energy. What's making you feel this way?",
        "pa": "ਮੈਨੂੰ ਬਹੁਤ ਖੁਸ਼ੀ ਹੈ ਕਿ ਤੁਸੀਂ ਚੰਗਾ ਮਹਿਸੂਸ ਕਰ ਰਹੇ ਹੋ, {name}! ਇਸ ਸਕਾਰਾਤਮਕ ਊਰਜਾ ਨੂੰ ਬਣਾਈ ਰੱਖੋ।"
    },
    "sadness": {
        "en": "I hear that you're feeling down, {name}. It's okay to feel this way sometimes. Remember, this too shall pass.",
        "pa": "ਮੈਂ ਸਮਝਦਾ ਹਾਂ ਕਿ ਤੁਸੀਂ ਉਦਾਸ ਮਹਿਸੂਸ ਕਰ ਰਹੇ ਹੋ, {name}। ਕਦੇ ਕਦੇ ਅਜਿਹਾ ਮਹਿਸੂਸ ਕਰਨਾ ਠੀਕ ਹੈ। ਯਾਦ ਰੱਖੋ, ਇਹ ਸਮਾਂ ਵੀ ਲੰਘ ਜਾਵੇਗਾ।"
    },
    "anger": {
        "en": "It sounds like you're really frustrated right now, {name}. Let's take a deep breath together.",
        "pa": "ਲੱਗਦਾ ਹੈ ਤੁਸੀਂ ਬਹੁਤ ਗੁੱਸੇ ਵਿੱਚ ਹੋ, {name}। ਆਓ ਇਕੱਠੇ ਲੰਬਾ ਸਾਹ ਲਈਏ।"
    },
    "fear": {
        "en": "It's completely normal to feel anxious or scared, {name}. You are in a safe space here.",
        "pa": "ਚਿੰਤਤ ਜਾਂ ਡਰਿਆ ਹੋਇਆ ਮਹਿਸੂਸ ਕਰਨਾ ਬਿਲਕੁਲ ਆਮ ਗੱਲ ਹੈ, {name}। ਤੁਸੀਂ ਇੱਥੇ ਸੁਰੱਖਿਅਤ ਹੋ।"
    },
    "surprise": {
        "en": "That sounds unexpected, {name}! How are you processing this?",
        "pa": "ਇਹ ਅਚਾਨਕ ਲੱਗਦਾ ਹੈ, {name}! ਤੁਸੀਂ ਇਸ ਬਾਰੇ ਕੀ ਸੋਚ ਰਹੇ ਹੋ?"
    },
    "disgust": {
        "en": "That sounds really unpleasant, {name}. Let's talk through it if you want.",
        "pa": "ਇਹ ਬਹੁਤ ਅਣਸੁਖਾਵਾਂ ਲੱਗਦਾ ਹੈ, {name}। ਜੇ ਤੁਸੀਂ ਚਾਹੋ ਤਾਂ ਆਓ ਇਸ ਬਾਰੇ ਗੱਲ ਕਰੀਏ।"
    },
    "neutral": {
        "en": "I'm listening, {name}. How's your day at GNDEC going? Any assignments or exams stressing you out?",
        "pa": "ਮੈਂ ਸੁਣ ਰਿਹਾ ਹਾਂ, {name}। GNDEC ਵਿੱਚ ਤੁਹਾਡਾ ਦਿਨ ਕਿਵੇਂ ਜਾ ਰਿਹਾ ਹੈ?"
    }
}

EMOTION_EMOJIS = {
    "joy": "😊", "sadness": "💙", "anger": "😤", "fear": "😨", "disgust": "🤢", "surprise": "😲", "neutral": "🧘"
}

EMOTION_COLORS = {
    "joy": "#FFD700", "sadness": "#4169E1", "anger": "#DC143C", 
    "fear": "#8B008B", "neutral": "#808080", "surprise": "#FF9933", 
    "disgust": "#006400"
}
