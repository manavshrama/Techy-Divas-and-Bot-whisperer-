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

# Application logic will go here
st.info("Built live at GNDEC Ludhiana Hackathon - Vibe Coding Session")
