# 🧡 ==========================================
# 🧡 MINDMITRA: GNDEC EDITION - UPDATED SKELETON
# 🧡 ==========================================
# 🤍 Built for the students of Guru Nanak Dev Engineering College, Ludhiana.
# 💚 ==========================================

import streamlit as st
from transformers import pipeline
from typing import Dict, List, Any, Tuple
import re
import time
import plotly.express as px
import pandas as pd

# ==========================================
# 🎨 UI & PAGE CONFIGURATION
# ==========================================

def setup_page():
    """
    Configures the MindMitra UI with a Saffron-White-Green vibe.
    """
    st.set_page_config(
        page_title="MindMitra: GNDEC Student Companion",
        page_icon="❤️",
        layout="wide"
    )

    # Custom CSS for the Saffron-White-Green Gradient Header & Chat Styles
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #f8f9fa;
        }
        .header-container {
            background: linear-gradient(90deg, #FF9933 0%, #FFFFFF 50%, #138808 100%);
            padding: 2.5rem;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        .header-title {
            color: #1e1e1e;
            font-size: 3.5rem;
            font-weight: 900;
            margin: 0;
            font-family: 'Inter', sans-serif;
        }
        .header-subtitle {
            color: #333;
            font-size: 1.3rem;
            margin-top: 10px;
            font-weight: 500;
        }
        .chat-container {
            max-width: 800px;
            margin: auto;
        }
        /* Custom sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid #e1e4e8;
        }
        </style>
        <div class="header-container">
            <h1 class="header-title">GNDEC Ludhiana Student Mental Health Companion ❤️</h1>
            <p class="header-subtitle">Ludhiana's first AI Mitra for campus stress, exam anxiety, and much more.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================
# 🧠 AI EMOTION ENGINE
# ==========================================

# Entering the GNDEC emotional zone - where Gill Road meets mental wellness.
@st.cache_resource(show_spinner="Connecting to MindMitra's emotional core...")
def initialize_feelings() -> Any:
    """
    Loads the emotion analysis model.
    Using: j-hartmann/emotion-english-distilroberta-base
    """
    try:
        feel_detector = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base"
        )
        return feel_detector
    except Exception as e:
        st.error(f"Error connecting to heart: {e}")
        return None

def detect_emotion(user_text: str, detector: Any) -> Tuple[str, str]:
    """
    Detects the primary emotion in given text and returns with emoji.
    """
    if not detector:
        return "neutral", "😐"
    
    emoji_map = {
        "joy": "😊", "sadness": "😢", "anger": "😤", 
        "fear": "😨", "surprise": "😲", "disgust": "🤢", "neutral": "😐"
    }
    
    try:
        feelings_raw = detector(user_text)
        mood_tag = feelings_raw[0]['label'].lower()
        return mood_tag, emoji_map.get(mood_tag, "😐")
    except Exception:
        return "neutral", "😐"

# ==========================================
# 💬 EMOTIONAL RESPONSES & REASONING
# ==========================================

EMOTION_RESPONSES: Dict[str, str] = {
    "joy": "Paaji chak de phatte! I'm so happy for you. This calls for a treat at the canteen! 🥳",
    "sadness": "Oho, dil chhota na kar mitra. Life has ups and downs, but GNDEC students are tough. We are in this together. ❤️",
    "anger": "I hear you, gussa aana natural hai. Take a deep breath. Focus on what we can control right now. 😤",
    "fear": "Darr lagna normal hai, especially with exams or placements. But remember, you've handled tough stuff before. Tention na lo. 👣",
    "surprise": "Whoa! Hairani wali gal hai! 😲 Sudden changes can be a lot, but let's see how we can handle this.",
    "disgust": "Eh gal bilkul theek nahi laggi. I understand why you're feeling this way. Speak your heart out. 🤐",
    "neutral": "I'm just vibing here with you. Tusi daso, hor ki chal reha campus te? Everything okay? 🤔"
}

CRISIS_KEYWORDS: List[str] = [
    "suicide", "kill myself", "want to die", "marna chahunda", "end it all",
    "self harm", "help me", "emergency", "zindagi khatam"
]

def check_crisis(text: str) -> bool:
    danger_check = False
    text_clean = text.lower()
    for word in CRISIS_KEYWORDS:
        if re.search(r'\b' + re.escape(word) + r'\b', text_clean):
            danger_check = True
            break
    return danger_check

# ==========================================
# 📊 SIDEBAR COMPONENT: YOUR MOOD JOURNEY
# ==========================================

def render_sidebar():
    with st.sidebar:
        st.title("🧡 Your Mood Journey")
        st.markdown("---")
        
        if st.session_state.mood_history:
            # Prepare data for Plotly pie chart
            mood_df = pd.DataFrame(st.session_state.mood_history, columns=["Mood"])
            mood_counts = mood_df["Mood"].value_counts().reset_index()
            mood_counts.columns = ["Mood", "Count"]

            # Slightly changed Plotly colors as requested (Saffron, White-ish, Green)
            custom_colors = ['#FF8C00', '#F5F5F5', '#228B22', '#FFD700', '#A9A9A9', '#CD5C5C']
            
            fig = px.pie(
                mood_counts, 
                values='Count', 
                names='Mood', 
                title='Feelings Overview',
                color_discrete_sequence=custom_colors,
                hole=0.4
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

            # Last 5 feelings
            st.subheader("Last 5 Feelings")
            for mood in st.session_state.mood_history[-5:][::-1]:
                st.write(f"- {mood.title()}")
        else:
            st.info("Start chatting to track your journey!")
            
        st.markdown("---")
        if st.button("Reset Everything"):
            st.session_state.messages = []
            st.session_state.mood_history = []
            st.rerun()

# ==========================================
# 🚀 MAIN APP EXECUTION
# ==========================================

def display_typing_effect(text: str):
    """Adds a simple typing animation for replies."""
    message_placeholder = st.empty()
    full_response = ""
    for char in text:
        full_response += char
        message_placeholder.markdown(full_response + "▌")
        time.sleep(0.01)
    message_placeholder.markdown(full_response)

def main():
    setup_page()
    
    # Initialize session states
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "mood_history" not in st.session_state:
        st.session_state.mood_history = []

    # Initialize Sidebar
    render_sidebar()
    
    # Initialize AI
    feel_detector = initialize_feelings()
    
    # Display Chat History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "mood" in msg:
                st.caption(f"Detected: {msg['mood']}")

    # User Input
    if prompt := st.chat_input("Kaun si gal karni hai, mitra? (Type here...)"):
        # Display User Message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Real-time Detection
        if check_crisis(prompt):
            mitra_bol = "### 🚨 Please reach out: **KIRAN Helpline (1800-599-0019)**. You are precious!."
            mood_label, emoji = "crisis", "❗"
        else:
            mood_label, emoji = detect_emotion(prompt, feel_detector)
            mitra_bol = EMOTION_RESPONSES.get(mood_label, EMOTION_RESPONSES["neutral"])
            st.session_state.mood_history.append(mood_label)

        # Display Assistant Message
        with st.chat_message("assistant"):
            display_typing_effect(mitra_bol)
            st.caption(f"Current Vibe: {mood_label.title()} {emoji}")
            
        st.session_state.messages.append({
            "role": "assistant", 
            "content": mitra_bol, 
            "mood": f"{mood_label.title()} {emoji}"
        })

if __name__ == "__main__":
    main()