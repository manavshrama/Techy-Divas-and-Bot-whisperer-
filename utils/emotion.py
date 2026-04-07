# Sinamor — emotion engine for MindMitra
# Using j-hartmann's distilroberta for 7-class emotion detection
# Cached so we don't reload 250MB model on every rerun

import streamlit as st
from transformers import pipeline


@st.cache_resource(show_spinner=False)
def _load_emotion_pipeline():
    """Load once, reuse forever. That's the Streamlit way."""
    return pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        return_all_scores=True,
        framework="pt"
    )


def analyze_emotion(text: str) -> list:
    """Returns list of {label, score} dicts for all 7 emotions."""
    if not text or not text.strip():
        return [{"label": "neutral", "score": 1.0}]
    pipe = _load_emotion_pipeline()
    return pipe(text)[0]


def check_crisis(text: str) -> bool:
    """
    Hard-coded keyword guard. This runs BEFORE the ML model.
    Sinamor: intentionally keeping this rule-based — no model should
    be trusted alone for suicide detection in a hackathon prototype.
    """
    danger_phrases = [
        "suicide", "kill myself", "end my life", "ending it",
        "harm myself", "hurt myself", "want to die", "wanna die",
        "worthless", "no reason to live", "better off dead",
        "can't go on", "won't wake up", "don't want to exist",
        # Punjabi / Hindi keywords
        "marna", "maut", "khatam", "jeena nahi",
        "mar jana", "zindagi khatam"
    ]
    txt = text.lower().strip()
    return any(phrase in txt for phrase in danger_phrases)


# ── Bilingual Response Bank ──────────────────────────────────
# Sinamor: kept the tone warm but not clinical — students hate
# feeling like they're talking to a therapist bot

EMOTION_RESPONSES = {
    "joy": {
        "en": "That's amazing, {name}! Hold onto this energy. What's making your day so good?",
        "pa": "ਬਹੁਤ ਵਧੀਆ, {name}! ਇਸ ਖੁਸ਼ੀ ਨੂੰ ਫੜ ਕੇ ਰੱਖੋ। ਕੀ ਚੱਲ ਰਿਹਾ ਵਧੀਆ?"
    },
    "sadness": {
        "en": "I hear you, {name}. It's okay to feel overwhelmed — you don't have to carry this alone.",
        "pa": "ਮੈਂ ਸਮਝਦਾ ਹਾਂ, {name}। ਉਦਾਸ ਹੋਣਾ ਠੀਕ ਹੈ — ਤੁਸੀਂ ਇਕੱਲੇ ਨਹੀਂ ਹੋ।"
    },
    "anger": {
        "en": "Your frustration is completely valid, {name}. Vent it out — I'm listening without judgment.",
        "pa": "ਤੁਹਾਡਾ ਗੁੱਸਾ ਸਮਝ ਆਉਂਦਾ ਹੈ, {name}। ਦੱਸੋ ਕੀ ਹੋਇਆ — ਮੈਂ ਸੁਣ ਰਿਹਾ ਹਾਂ।"
    },
    "fear": {
        "en": "Things can feel scary, {name}, but you're in a safe space right now. One step at a time.",
        "pa": "ਡਰ ਲੱਗਣਾ ਆਮ ਗੱਲ ਹੈ, {name}। ਤੁਸੀਂ ਇੱਥੇ ਸੁਰੱਖਿਅਤ ਹੋ — ਇੱਕ ਕਦਮ ਕਰਕੇ ਚੱਲੀਏ।"
    },
    "surprise": {
        "en": "Whoa, didn't see that coming! How are you processing this, {name}?",
        "pa": "ਇਹ ਤਾਂ ਅਚਾਨਕ ਹੋ ਗਿਆ, {name}! ਤੁਸੀਂ ਕੀ ਸੋਚ ਰਹੇ ਹੋ ਇਸ ਬਾਰੇ?"
    },
    "disgust": {
        "en": "That sounds really unpleasant, {name}. You don't have to tolerate things that feel wrong.",
        "pa": "ਇਹ ਬਹੁਤ ਮਾੜਾ ਲੱਗਦਾ ਹੈ, {name}। ਤੁਹਾਨੂੰ ਗਲਤ ਚੀਜ਼ਾਂ ਬਰਦਾਸ਼ਤ ਨਹੀਂ ਕਰਨੀਆਂ ਚਾਹੀਦੀਆਂ।"
    },
    "neutral": {
        "en": "I'm right here, {name}. How are the classes and assignments going? Anything bugging you?",
        "pa": "ਮੈਂ ਇੱਥੇ ਹਾਂ, {name}। ਕਲਾਸਾਂ ਕਿਵੇਂ ਚੱਲ ਰਹੀਆਂ? ਕੋਈ ਗੱਲ ਪਰੇਸ਼ਾਨ ਕਰ ਰਹੀ?"
    }
}

EMOTION_EMOJIS = {
    "joy": "🌟", "sadness": "🌧️", "anger": "🔥",
    "fear": "🛡️", "disgust": "🤚", "surprise": "⚡", "neutral": "🍃"
}

EMOTION_COLORS = {
    "joy": "#F59E0B", "sadness": "#3B82F6", "anger": "#EF4444",
    "fear": "#8B5CF6", "neutral": "#9CA3AF", "surprise": "#10B981",
    "disgust": "#059669"
}
