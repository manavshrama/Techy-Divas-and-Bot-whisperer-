# Sinamor
import streamlit as st
import os
import pandas as pd
import plotly.express as px
import time
from utils.emotion import analyze_emotion, check_crisis, EMOTION_RESPONSES, EMOTION_EMOJIS, EMOTION_COLORS
from utils.pdf_report import generate_pdf_report
from utils.voice import speech_to_text, text_to_speech

# Set page config
st.set_page_config(page_title="MindMitra GNDEC Edition", page_icon="🧘", layout="wide")

# 1. Initialize session state
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
    <p style="color: #333333; font-weight: bold; margin: 5px 0 0 0;">Dedicated to the Mental Wellness of Engineering Students</p>
</div>
""", unsafe_allow_html=True)

# Custom CSS
st.markdown("""
<style>
    /* Styling */
    [data-testid="stSidebar"] {
        background-color: #FFF3E0;
    }
    .stChatInputContainer {
        border: 2px solid #FF9933 !important;
    }
    [data-testid="stChatMessage"]:nth-child(even) { /* Bot */
        background-color: #F0FFF0;
        border-radius: 15px;
    }
    [data-testid="stChatMessage"]:nth-child(odd) { /* User */
        background-color: #FFF8F0;
        border-radius: 15px;
    }
</style>
""", unsafe_allow_html=True)

# sidebar content
with st.sidebar:
    st.image("https://gndec.ac.in/logo.png", width=100) # Assumes GNDEC logo or placeholder
    st.title("GNDEC Buddy 🫂")
    st.write(f"Hello, **{st.session_state.user_name}**!")
    
    new_name = st.text_input("What should I call you?", st.session_state.user_name)
    if new_name != st.session_state.user_name:
        st.session_state.user_name = new_name
        st.rerun()

    st.divider()
    with st.expander("🌿 Quick Grounding Exercise"):
        st.write("""
        **5-4-3-2-1 Technique:**
        - **5** things you can **see**
        - **4** things you can **feel**
        - **3** things you can **hear**
        - **2** things you can **smell**
        - **1** thing you can **taste**
        """)
        if st.button("Start Timer ▶"):
            countdown_display = st.empty()
            for i in range(30, 0, -1):
                countdown_display.markdown(f"## ⏳ {i}s")
                time.sleep(1)
            countdown_display.success("Ghera saah lavo. (Take a deep breath.) 🧘")

# Helplines Constant
INDIAN_HELPLINES = {
    "Vandrevala Foundation": "9999666555",
    "AASRA": "9820466726",
    "iCall": "9152987821",
    "NIMHANS": "08046110007"
}

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Supportive Chat")
    
    # Display message history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Voice Input Section
    if st.button("🎤 Voice Input (Microphone required)"):
        with st.spinner("Listening..."):
            heard_text = speech_to_text()
            if heard_text:
                st.success(f"Heard: {heard_text}")
                st.info("Please paste the heard text below if it's correct.")

    # Main Chat Input
    if prompt := st.chat_input("How are you feeling today?"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Crisis detection
        if check_crisis(prompt):
            with st.chat_message("assistant"):
                crisis_markup = """
                <div style="background-color: #FFCDD2; padding: 25px; border-radius: 15px; border-left: 10px solid #D32F2F;">
                    <h2 style="color: #B71C1C; margin-top: 0;">🛑 Ruk. Take a moment.</h2>
                    <p style="font-size: 1.1em; color: #B71C1C;"><b>Tusi akale nahi ho.</b> We care about you. Please reach out to these helplines right now:</p>
                    <ul style="list-style-type: none; padding: 0;">
                """
                for provider, phone in INDIAN_HELPLINES.items():
                    crisis_markup += f"<li><b>📞 {provider}:</b> {phone}</li>"
                
                crisis_markup += """
                    </ul>
                    <div style="margin-top: 15px; font-weight: bold;">
                        📍 GNDEC Counseling Cell: Visit Admin Block, Room 102.
                    </div>
                </div>
                """
                st.markdown(crisis_markup, unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": "⚠️ Crisis Resources shared."})
        else:
            with st.chat_message("assistant"):
                with st.spinner("Analyzing..."):
                    # Updated on 2026-04-07 by Antigravity - refining emotion extraction
                    results = analyze_emotion(prompt)
                    dominant_emotion_info = max(results, key=lambda x: x['score'])
                    label = dominant_emotion_info['label']
                    score = dominant_emotion_info['score']
                    emoji = EMOTION_EMOJIS.get(label, "🧘")
                    
                    # Update mood history
                    st.session_state.mood_history.append({"label": label, "timestamp": time.time()})
                    
                    # Get responses
                    emotion_response_data = EMOTION_RESPONSES.get(label, EMOTION_RESPONSES["neutral"])
                    response_en = emotion_response_data["en"].format(name=st.session_state.user_name)
                    response_pa = emotion_response_data["pa"].format(name=st.session_state.user_name)
                    
                    full_response = f"### Detected Mood: {emoji} **{label.capitalize()}**\n\n"
                    full_response += f"**English Support:**\n{response_en}\n\n"
                    full_response += f"**Punjabi Support:**\n{response_pa}"
                    
                    st.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    
                    # Store variables for analytics update
                    st.session_state.last_results = results

with col2:
    st.subheader("📊 Insights")
    
    if "last_results" in st.session_state:
        df = pd.DataFrame(st.session_state.last_results)
        fig = px.bar(df, x='label', y='score', 
                     title="Emotion Profile", 
                     color='label',
                     color_discrete_map=EMOTION_COLORS)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Talk to me to see your emotion profile.")

    st.divider()
    st.subheader("📄 Daily Summary")
    
    if st.button("Generate Report"):
        if st.session_state.messages:
            summary_text = f"Report for User: {st.session_state.user_name}\n\n"
            summary_text += "Conversation Log:\n"
            for msg in st.session_state.messages:
                summary_text += f"[{msg['role'].upper()}]: {msg['content']}\n"
            
            try:
                pdf_bytes = generate_pdf_report(summary_text)
                st.download_button(
                    label="📥 Download Session PDF",
                    data=pdf_bytes,
                    file_name=f"MindMitra_Session.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error generating PDF: {e}")
        else:
            st.warning("Chat with me first!")

    st.markdown("---")
    st.caption("Developed for GNDEC Students.")
