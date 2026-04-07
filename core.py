# 🧡 ==========================================
# 🧡 SAFFRON: MINDMITRA GNDEC EDITION - SETUP
# 🧡 ==========================================
# 🤍 Run the following command in a Colab cell to install dependencies:
# 🤍 !pip install streamlit transformers torch plotly pandas speechrecognition pyttsx3 localtunnel
# 💚 ==========================================
# 💚 GREEN: READY FOR VIBE CODING AT GNDEC
# 💚 ==========================================

import streamlit as st
from transformers import pipeline
from typing import Dict, Tuple, Any, List
import re

# ==========================================
# CONFIGURATION & PREMIUM STYLING
# ==========================================

def setup_page() -> None:
    """
    Configures the Streamlit page with premium aesthetics.
    Includes:
    - Wide layout & page icon
    - Google Fonts (Inter) integration
    - Custom Tricolor (Saffron-White-Green) Gradient Header
    """
    st.set_page_config(
        page_title="MindMitra GNDEC Edition",
        page_icon="❤️",
        layout="wide"
    )

    # Injecting modern typography and tricolor vibes
    st.markdown(
        """
        <style>
        /* Import Google Fonts for a premium look */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .main-header {
            background: linear-gradient(135deg, #FF9933 0%, #FFFFFF 50%, #138808 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-family: 'Inter', sans-serif;
            font-size: 3.5rem;
            font-weight: 800;
            text-align: center;
            margin-bottom: 0.5rem;
            text-shadow: 2px 4px 6px rgba(0,0,0,0.05);
        }

        .sub-header {
            text-align: center;
            font-size: 1.2rem;
            color: #4A4A4A;
            font-weight: 400;
            margin-bottom: 2rem;
            letter-spacing: 1px;
        }

        /* Smooth glassy divider */
        .divider {
            height: 2px;
            background: linear-gradient(to right, transparent, #ccc, transparent);
            margin: 20px 0;
        }
        </style>
        
        <div class="main-header">MindMitra GNDEC Edition ❤️</div>
        <div class="sub-header">Your empathetic campus companion for the students of Punjab.</div>
        <div class="divider"></div>
        """,
        unsafe_allow_html=True
    )

# ==========================================
# AI MODEL INFRASTRUCTURE (CACHED)
# ==========================================

@st.cache_resource(show_spinner="Connecting to MindMitra's emotional core...")
def load_emotion_model() -> Any:
    """
    Loads and caches the DistilRoBERTa emotion detection pipeline.
    Model: j-hartmann/emotion-english-distilroberta-base
    """
    try:
        emotion_pipe = pipeline(
            "text-classification", 
            model="j-hartmann/emotion-english-distilroberta-base"
        )
        return emotion_pipe
    except Exception as e:
        st.error(f"Error loading emotion model: {e}")
        return None

# ==========================================
# BILINGUAL EMOTIONAL INTELLIGENCE
# ==========================================

def get_emotion_responses() -> Dict[str, str]:
    """
    Returns a dictionary of empathetic responses in a 'Hinglish/Punjabi' mix.
    """
    return {
        "joy": (
            "I'm so happy for you! Khushi di gal hai! 😊 "
            "Whether it's a cracked interview or a cancelled lecture, you deserve to celebrate."
        ),
        "sadness": (
            "I hear you, and it's okay to feel low. Udas na ho mitra. ❤️ "
            "Engineering life handles a lot—practicals, attendance, stress."
        ),
        "anger": "That sounds really frustrating. Gussa aana normal hai. 😤",
        "fear": "It's completely normal to feel a bit anxious. Darr lagna aam gal hai.",
        "surprise": "Whoa, unexpected change can be a shock! Hairani wali gal hai. 😲",
        "disgust": "I can tell you're really put off by something. Eh gal theek nahi laggi tenu.",
        "neutral": "I'm right here with you. Sab theek chal reha hai?"
    }

# ==========================================
# SAFETY & CRISIS PROTOCOLS
# ==========================================

def get_crisis_info() -> str:
    """Returns formatted Indian crisis helplines."""
    return (
        "### 🚨 **CRISIS SUPPORT: Please reach out!** 🚨\n"
        "- **KIRAN Helpline**: **1800-599-0019** (24x7)\n"
        "- **Vandrevala**: **9999 666 555**\n"
        "--- \n"
        "*Your life is incredibly precious.*"
    )

def check_crisis_keywords(user_input: str) -> bool:
    """Checks for high-risk crisis keywords."""
    crisis_keywords: List[str] = ["suicide", "kill myself", "want to die", "marna chahunda"]
    text_lower = user_input.lower()
    for word in crisis_keywords:
        if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
            return True
    return False

def analyze_and_respond(user_input: str, emotion_model: Any) -> Tuple[str, str, bool]:
    """Processes user input for emotions and crisis."""
    is_crisis = check_crisis_keywords(user_input)
    if is_crisis:
        return ("critical", get_crisis_info(), True)
    
    if not emotion_model:
        return ("neutral", "How are you feeling?", False)
        
    try:
        results = emotion_model(user_input)
        predicted_label = results[0]['label'].lower()
    except Exception:
        predicted_label = "neutral"
        
    responses = get_emotion_responses()
    response_text = responses.get(predicted_label, responses["neutral"])
    
    return (predicted_label, response_text, False)