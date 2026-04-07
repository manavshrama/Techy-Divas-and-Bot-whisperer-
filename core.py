import streamlit as st
from transformers import pipeline
from typing import Dict, Tuple, Any
import re

# ==========================================
# CONFIGURATION & SETUP
# ==========================================

def setup_page() -> None:
    """
    Configures the Streamlit page layout, title, and initial styles.
    Sets up the Indian tricolor (saffron-white-green) gradient header.
    """
    st.set_page_config(
        page_title="MindMitra GNDEC Edition",
        page_icon="❤️",
        layout="wide"
    )

    # Tricolor gradient header (Saffron, White, Green) with GNDEC vibes
    st.markdown(
        """
        <style>
        .header-gradient {
            background: linear-gradient(to right, #FF9933, #FFFFFF, #138808);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            padding: 20px 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        </style>
        <div class="header-gradient">MindMitra GNDEC Edition ❤️</div>
        <p style='text-align: center; font-size: 1.2rem; color: #555;'>Your campus mental health companion.</p>
        """,
        unsafe_allow_html=True
    )

# ==========================================
# MODEL LOADING
# ==========================================

@st.cache_resource(show_spinner="Loading MindMitra's AI model...")
def load_emotion_model() -> Any:
    """
    Loads the DistilRoBERTa emotion detection model and caches it.
    Caching prevents reloading the large model on every Streamlit rerun.
    """
    # Pipeline for text-classification maps to the 7 core emotions
    emotion_pipeline = pipeline(
        "text-classification", 
        model="j-hartmann/emotion-english-distilroberta-base"
    )
    return emotion_pipeline

# ==========================================
# DICTIONARIES & HELPLINES
# ==========================================

def get_emotion_responses() -> Dict[str, str]:
    """
    Returns a dictionary of empathetic responses paired with emotions.
    Responses are tailored for Punjab engineering students (English + simple Punjabi mix).
    """
    return {
        "joy": "That's wonderful! Khushi di gal hai! 😊 Keep that positive energy glowing. What made you feel this way today?",
        "sadness": "I hear you, and it's okay to feel sad. Udas na ho, exams ya assignments di tension ho sakdi hai. Take a deep breath. Would you like to talk more about what's weighing on your mind?",
        "anger": "It sounds like you're really frustrated right now. Gussa aana natural hai. Panga lain ton pehlan, let's take a step back and vent it out here. I'm listening.",
        "fear": "It's completely normal to feel anxious or scared, especially with college pressures. Darr lagna aam gal hai. Let's break down what's worrying you together. You're not alone.",
        "surprise": "Wow, unexpected things can really throw us off! Hairani wali gal theek hai. Take a moment to process it. Is it a good surprise or a stressful one?",
        "disgust": "I understand that something is really bothering you or feeling unpleasant. Eh gal theek nahi laggi tenu. Do you want to share what made you feel this way?",
        "neutral": "I'm right here with you. Sab theek chal reha hai? Whether you want to rant about practicals, or just chill, I'm all ears."
    }

def get_crisis_info() -> str:
    """
    Provides Indian/Punjab emergency helpline information formatted for easy reading.
    """
    return (
        "🚨 **CRISIS ALERT: We are here for you!** 🚨\n\n"
        "Please remember that you don't have to face this alone. Reach out to someone who can help immediately:\n"
        "- **KIRAN Mental Health Helpline**: 1800-599-0019 (24x7, Toll-Free)\n"
        "- **Vandrevala Foundation**: 9999 666 555 (24x7)\n"
        "- **AASRA**: 9820466726\n"
        "- **GNDEC Student Counseling Cell**: [Contact your mentor or HOD immediately]\n\n"
        "*Please talk to a trusted friend, family member, or professional right away. Your life is precious.*"
    )

# ==========================================
# CORE LOGIC FUNCTIONS
# ==========================================

def check_crisis_keywords(user_input: str) -> bool:
    """
    Checks if the user's input contains any high-risk crisis keywords.
    """
    crisis_keywords = [
        "suicide", "kill myself", "want to die", "end my life", 
        "worthless", "give up", "harm myself", "no reason to live"
    ]
    
    # Convert input to lowercase for case-insensitive matching
    text_lower = user_input.lower()
    
    for word in crisis_keywords:
        # Check for complete word matches
        if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
            return True
            
    return False

def analyze_and_respond(user_input: str, emotion_model: Any) -> Tuple[str, str, bool]:
    """
    Processes the user input systematically:
    1. Checks for crisis keywords first.
    2. Analyzes emotions if no crisis is detected.
    3. Generates an empathetic, bilingual response.
    
    Returns:
        Tuple containing (emotion_label, response_text, is_crisis)
    """
    # 1. Prioritize Crisis Check
    is_crisis = check_crisis_keywords(user_input)
    if is_crisis:
        return ("critical", get_crisis_info(), True)
        
    # 2. Emotion Analysis
    try:
        results = emotion_model(user_input)
        # Results format typically: [{'label': 'joy', 'score': 0.99}]
        predicted_emotion = results[0]['label']
    except Exception:
        # Fallback to neutral in case of inference error
        predicted_emotion = "neutral"
        
    # 3. Response Generation
    responses = get_emotion_responses()
    # Default to neutral if the model outputs something unexpected
    response_text = responses.get(predicted_emotion, responses["neutral"])
    
    return (predicted_emotion, response_text, False)
