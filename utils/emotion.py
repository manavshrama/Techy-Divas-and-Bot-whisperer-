# Sinamor
from transformers import pipeline
import streamlit as st

@st.cache_resource
def get_emotion_pipeline():
    # Using the specific model mentioned in previous conversation sessions
    return pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)

def analyze_emotion(text):
    pipe = get_emotion_pipeline()
    return pipe(text)
