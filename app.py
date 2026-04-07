# Sinamor
# Sinamor: Setting up the vibe with a wide layout and a green heart 💚
# Sinamor: The tricolor header is a must! Punjab represent, India represent!
# Sinamor: Every GNDEC student should feel at home when they open this. 🧘‍♂️

import streamlit as st
import os
import pandas as pd
import plotly.express as px
import datetime
import time
from utils.emotion import analyze_emotion, get_top_emotion, check_crisis, EMOTION_RESPONSES, EMOTION_EMOJIS, EMOTION_COLORS

# Set page config
st.set_page_config(
    page_title="MindMitra GNDEC", 
    page_icon="💚", 
    layout="wide"
)

# Sinamor: 1. Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "mood_history" not in st.session_state:
    st.session_state.mood_history = []
if "user_name" not in st.session_state:
    st.session_state.user_name = "Yaar"

# Custom HTML Header
st.markdown("""
<div style="background: linear-gradient(90deg, #FF9933 0%, #FFFFFF 50%, #138808 100%); 
            padding: 20px; border-radius: 10px; border: 2px solid #ccc; text-align: center; margin-bottom: 25px;">
    <h1 style="color: #000080; margin: 0; font-family: 'Inter', sans-serif;">MindMitra GNDEC Edition 🧘</h1>
    <p style="color: #333333; font-weight: bold; margin: 5px 0 0 0;">Dedicated to the Mental Wellness of Ludhiana Students</p>
</div>
""", unsafe_allow_html=True)

# Custom CSS (Sinamor's Personal Touch)
st.markdown("""
<style>
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFF3E0;
    }
    
    /* Chat Input Border */
    .stChatInputContainer {
        border: 2px solid #FF9933 !important;
    }
    
    /* Message Bubbles */
    [data-testid="stChatMessage"]:nth-child(even) { /* Bot */
        background-color: #F0FFF0;
        border-radius: 15px;
    }
    [data-testid="stChatMessage"]:nth-child(odd) { /* User */
        background-color: #FFF8F0;
        border-radius: 15px;
    }
    
    /* Sinamor's Touch: Animated Header Pulse */
    @keyframes pulse {
        0% { opacity: 0.8; }
        50% { opacity: 1; }
        100% { opacity: 0.8; }
    }
    .stHeader {
        animation: pulse 3s infinite ease-in-out;
    }
    
    /* Footer Styling */
    .footer {
        color: gray;
        text-align: center;
        font-size: 0.8em;
        margin-top: 50px;
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Sinamor: 3. Sidebar Grounding Exercise
with st.sidebar:
    st.divider()
    with st.expander("🌿 30-Second Grounding Exercise"):
        st.write("""
        **5-4-3-2-1 Technique:**
        - **5** things you can **see**
        - **4** things you can **feel**
        - **3** things you can **hear**
        - **2** things you can **smell**
        - **1** thing you can **taste**
        """)
        if st.button("Start Timer ▶"):
            timer_placeholder = st.empty()
            for i in range(30, 0, -1):
                timer_placeholder.markdown(f"## ⏳ {i}s")
                time.sleep(1)
            timer_placeholder.success("Aram naal saah lao. (Take a deep breath.) 🧘")

# Helplines Constant
INDIAN_HELPLINES = {
    "Vandrevala Foundation": "9999666555",
    "AASRA": "9820466726",
    "iCall": "9152987821",
    "NIMHANS": "08046110007"
}

# rest of the logic

if prompt := st.chat_input("Dasso kya ho raha hai..."):
    # (previous logic for messages and feelings remains)
    
    with st.chat_message("assistant"):
        if is_crisis:
            # Sinamor: 1. Crisis Handling Upgrade
            st.markdown("""
            <div style="background-color: #FFCDD2; padding: 25px; border-radius: 15px; border-left: 10px solid #D32F2F;">
                <h2 style="color: #B71C1C; margin-top: 0;">🛑 Ruk. Ik minute.</h2>
                <p style="font-size: 1.2em; font-weight: bold; color: #B71C1C;">Tenu pyaar hai. Tu akela nahin.</p>
                <p>Please talk to someone right now. Yeh message save kar lo.</p>
                <hr style="border-top: 1px solid #B71C1C;">
                <ul style="list-style-type: none; padding: 0;">
            """, unsafe_allow_html=True)
            
            for provider, phone in INDIAN_HELPLINES.items():
                st.markdown(f"**📞 {provider}:** {phone}")
            
            st.markdown("""
                </ul>
                <div style="margin-top: 15px; font-weight: bold;">
                    📍 GNDEC Student Counseling Cell: Visit Admin Block, Room 102.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Sinamor: No bot reply when crisis is detected
            st.session_state.messages.append({"role": "assistant", "content": "⚠️ Crisis Alert: Help Resources Provided."})
        else:
            # (normal bot reply streaming)
            pass

# Footer
st.markdown("""
<div class="footer">
    Made live in 8 hours · GNDEC Ludhiana · Sinamor · Mental health matters 💚
</div>
""", unsafe_allow_html=True)
