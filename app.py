# Sinamor
import streamlit as st
import os
import pandas as pd
import plotly.express as px
from utils.emotion import analyze_emotion
from utils.pdf_report import generate_pdf_report
from utils.voice import speech_to_text, text_to_speech

# Set page config
st.set_page_config(page_title="MindMitra GNDEC Edition", page_icon="🧘", layout="wide")

st.markdown("""
<div style="background: linear-gradient(to right, #FF9933, #FFFFFF, #138808); padding: 10px; border-radius: 5px; text-align: center;">
    <h1 style="color: black;">MindMitra GNDEC Edition 🧘</h1>
    <p style="color: black; font-weight: bold;">Empowering GNDEC Ludhiana Engineering Students</p>
</div>
""", unsafe_allow_html=True)

# Bilingual Response Dictionary for common emotions
RESPONSES = {
    "joy": {
        "en": "I'm so glad you're feeling good! Keep up the positive energy. What's making you feel this way?",
        "pa": "ਮੈਨੂੰ ਬਹੁਤ ਖੁਸ਼ੀ ਹੈ ਕਿ ਤੁਸੀਂ ਚੰਗਾ ਮਹਿਸੂਸ ਕਰ ਰਹੇ ਹੋ! ਇਸ ਸਕਾਰਾਤਮਕ ਊਰਜਾ ਨੂੰ ਬਣਾਈ ਰੱਖੋ।"
    },
    "sadness": {
        "en": "I hear that you're feeling down. It's okay to feel this way sometimes. Remember, this too shall pass.",
        "pa": "ਮੈਂ ਸਮਝਦਾ ਹਾਂ ਕਿ ਤੁਸੀਂ ਉਦਾਸ ਮਹਿਸੂਸ ਕਰ ਰਹੇ ਹੋ। ਕਦੇ ਕਦੇ ਅਜਿਹਾ ਮਹਿਸੂਸ ਕਰਨਾ ਠੀਕ ਹੈ। ਯਾਦ ਰੱਖੋ, ਇਹ ਸਮਾਂ ਵੀ ਲੰਘ ਜਾਵੇਗਾ।"
    },
    "anger": {
        "en": "It sounds like you're really frustrated right now. Let's take a deep breath together.",
        "pa": "ਲੱਗਦਾ ਹੈ ਤੁਸੀਂ ਬਹੁਤ ਗੁੱਸੇ ਵਿੱਚ ਹੋ। ਆਓ ਇਕੱਠੇ ਲੰਬਾ ਸਾਹ ਲਈਏ।"
    },
    "fear": {
        "en": "It's completely normal to feel anxious or scared. You are in a safe space here.",
        "pa": "ਚਿੰਤਤ ਜਾਂ ਡਰਿਆ ਹੋਇਆ ਮਹਿਸੂਸ ਕਰਨਾ ਬਿਲਕੁਲ ਆਮ ਗੱਲ ਹੈ। ਤੁਸੀਂ ਇੱਥੇ ਸੁਰੱਖਿਅਤ ਹੋ।"
    },
    "surprise": {
        "en": "That sounds unexpected! How are you processing this?",
        "pa": "ਇਹ ਅਚਾਨਕ ਲੱਗਦਾ ਹੈ! ਤੁਸੀਂ ਇਸ ਬਾਰੇ ਕੀ ਸੋਚ ਰਹੇ ਹੋ?"
    },
    "disgust": {
        "en": "That sounds really unpleasant. Let's talk through it if you want.",
        "pa": "ਇਹ ਬਹੁਤ ਅਣਸੁਖਾਵਾਂ ਲੱਗਦਾ ਹੈ। ਜੇ ਤੁਸੀਂ ਚਾਹੋ ਤਾਂ ਆਓ ਇਸ ਬਾਰੇ ਗੱਲ ਕਰੀਏ।"
    },
    "neutral": {
        "en": "I'm listening. How's your day at GNDEC going? Any assignments or exams stressing you out?",
        "pa": "ਮੈਂ ਸੁਣ ਰਿਹਾ ਹਾਂ। GNDEC ਵਿੱਚ ਤੁਹਾਡਾ ਦਿਨ ਕਿਵੇਂ ਜਾ ਰਿਹਾ ਹੈ?"
    }
}

CRISIS_HELPLINES = """
### 🚨 Emergency Resources & Helplines (India)
If you or someone you know is feeling overwhelmed or in crisis, please reach out for professional help immediately:
- **AASRA (Crisis Intervention & Suicide Prevention):** +91-9820466726
- **Vandrevala Foundation (Mental Health Helpline):** +91-9999 666 555
- **Kiran (Mental Health Helpline by Govt. of India):** 1800-599-0019
- **GNDEC Student Guidance & Counseling Cell:** Make sure to visit the counseling center on campus.
"""

st.info("Built live at GNDEC Ludhiana - Empowering mental wellbeing of engineering students locally.")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Chat with MindMitra")
    
    # Text Input
    user_input = st.text_area("How are you feeling today? Share your thoughts...", height=100)
    
    # Voice Input Button (Mockup logic for Streamlit as direct mic access needs a custom component to work perfectly in browser)
    if st.button("🎤 Or click here to Speak (Requires local mic access)"):
        with st.spinner("Listening..."):
            user_input = speech_to_text()
            st.success(f"Heard: {user_input}")

    if st.button("Analyze & Respond"):
        if user_input.strip():
            with st.spinner("Analyzing your emotions..."):
                results = analyze_emotion(user_input)
                
                # The model returns a list of lists of dictionaries. We sort by highest score.
                # E.g., [[{'label': 'sadness', 'score': 0.9}, ...]]
                emotions = results[0]
                top_emotion = max(emotions, key=lambda x: x['score'])
                
                emotion_label = top_emotion['label']
                emotion_score = top_emotion['score']
                
                st.write(f"### Detected Emotion: **{emotion_label.capitalize()}** (Confidence: {emotion_score:.2f})")
                
                response_en = RESPONSES.get(emotion_label, RESPONSES["neutral"])["en"]
                response_pa = RESPONSES.get(emotion_label, RESPONSES["neutral"])["pa"]
                
                st.success(f"**English Response:**\n\n{response_en}")
                st.info(f"**Punjabi Response:**\n\n{response_pa}")
                
                # Optional TTS
                # text_to_speech(response_en) # Consider uncommenting if evaluating locally
                
                # Trigger Crisis Protocol if dealing with severe negative emotions with high confidence
                if emotion_label in ['sadness', 'fear'] and emotion_score > 0.8:
                    st.error("It seems you are going through a tough time.")
                    st.markdown(CRISIS_HELPLINES)
                    
        else:
            st.warning("Please type something or use the voice input to share your thoughts.")

with col2:
    st.subheader("📊 Emotion Analytics")
    st.write("Track your emotional journey (Demo)")
    
    # Placeholder for Chart
    if user_input and 'results' in locals() and results:
        df = pd.DataFrame(results[0])
        fig = px.bar(df, x='label', y='score', title="Current Emotion Distribution", color='label')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Share your thoughts to see your emotion analytics graphic here!")
    
    st.write("---")
    st.markdown(CRISIS_HELPLINES)
    
    if st.button("Download Session PDF Report"):
        # Dummy summary for the PDF
        pdf_bytes = generate_pdf_report("User discussed feeling their current state. Emotion detected.")
        st.download_button(
            label="📄 Download Report",
            data=pdf_bytes,
            file_name="MindMitra_Session_Report.pdf",
            mime="application/pdf"
        )
