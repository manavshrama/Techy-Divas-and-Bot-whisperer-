# MindMitra: GNDEC Edition 🧘

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mindmitra-gndec.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Transformers](https://img.shields.io/badge/HuggingFace-Transformers-yellow?style=for-the-badge&logo=huggingface)

**MindMitra** is a premium, AI-powered mental wellness companion specifically designed for engineering students at **GNDEC Ludhiana**. It provides an anonymous, safe space to vent frustrations, track moods, and receive empathetic support in both English and Punjabi.

---

## 🚀 Key Features

- **🧠 Real-time Emotion Analysis**: Powered by DistilRoBERTa to detect 7 distinct emotional states.
- **🛡️ Crisis Triage System**: Immediate, non-negotiable safety UI if self-harm intent is detected, linking to 24/7 Indian helplines.
- **🗣️ Bilingual Empathy**: Natural, warm responses tailored in English and Punjabi (Ma Boli).
- **📉 Live Mood Radar**: Visual breakdown of your current psychological state using Plotly.
- **🎤 Voice Connect**: Hands-free interaction using Google's Speech Recognition API.
- **🌿 Grounding Tools**: Built-in 5-4-3-2-1 sensory exercises with interactive timers to combat anxiety.
- **📄 Session Vault**: Export your chat session into a secure, sanitized PDF report.

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **ML Engine**: HuggingFace Transformers (j-hartmann/emotion-english-distilroberta-base)
- **Visuals**: Plotly Express
- **Audio**: SpeechRecognition, PyAudio, Pyttsx3
- **Export**: FPDF2

---

## 💻 Local Setup

1. **Clone the Repo**
   ```bash
   git clone https://github.com/manavshrama/mindmitra.git
   cd mindmitra
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   *Note: For voice support on Windows, you may need: `pip install pipwin && pipwin install pyaudio`*

3. **Launch App**
   ```bash
   streamlit run app.py
   ```

---

## ☁️ Deployment

### Option A: Streamlit Cloud (Recommended)
1. Push your code to GitHub.
2. Sign in to [Streamlit Share](https://share.streamlit.io/).
3. Connect your repository and deploy `app.py`.

### Option B: Docker
```bash
docker build -t mindmitra .
docker run -p 8501:8501 mindmitra
```

---

## 🏆 Hackathon Note
Built with ❤️ by **Sinamor** in just 8 hours for the GNDEC Ludhiana Hackathon (2026-04-07). Dedicated to the mental wellness of every student walking the halls of Gill Park.

---
*Disclaimer: This is an AI companion, not a replacement for professional medical advice.*
