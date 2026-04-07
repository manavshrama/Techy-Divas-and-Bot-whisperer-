# MindMitra GNDEC Edition 🧘

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-F9AB00?style=for-the-badge&logo=huggingface&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)

> **An anonymous, AI-powered mental wellness companion built for engineering students in Punjab.**

MindMitra detects emotions in real-time using transformer models, provides bilingual (English + Punjabi) empathetic responses, and features a robust crisis detection system that immediately routes students to verified Indian helplines.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🧠 **Emotion Detection** | 7-class sentiment analysis via `j-hartmann/emotion-english-distilroberta-base` |
| 🛑 **Crisis Safety Override** | Keyword-based guard that overrides AI and shows emergency helplines instantly |
| 🗣️ **Bilingual Responses** | Warm, localized replies in English and Punjabi |
| 📊 **Live Emotion Radar** | Real-time Plotly visualization of detected sentiments |
| 📈 **Mood Trend Tracker** | Session-based pie chart in sidebar tracking emotional patterns |
| ✍️ **Typing Animation** | Word-by-word streaming for natural conversation feel |
| 📄 **PDF Export** | Download session transcript as a formatted, sanitized PDF |
| 🎙️ **Voice Input** | Mic support via SpeechRecognition (graceful fallback if unavailable) |
| 🌿 **Grounding Exercise** | Built-in 5-4-3-2-1 technique with 30-second breathing timer |
| 🎨 **Premium India-themed UI** | Tricolor accents, glassmorphism header, custom chat bubbles |

---

## 📁 Project Structure

```
mindmitra/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies (pinned)
├── README.md               # You're reading this
├── Dockerfile              # Container deployment
├── .dockerignore
├── .streamlit/
│   └── config.toml         # Theme & server config
└── utils/
    ├── emotion.py           # Emotion model + crisis detection + responses
    ├── pdf_report.py        # PDF generation with fpdf2
    └── voice.py             # Speech-to-text with graceful fallback
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
git clone https://github.com/manavshrama/mindmitra.git
cd mindmitra
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### Run Locally

```bash
streamlit run app.py
```

App opens at `http://localhost:8501` 🎉

---

## ☁️ Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Click **New App** → Connect your GitHub repo
4. Set main file path to `app.py`
5. Click **Deploy**

Streamlit Cloud automatically reads `requirements.txt` and `.streamlit/config.toml`.

> **Note:** Voice input (PyAudio) won't work on Streamlit Cloud — the app gracefully handles this with a user-friendly error message.

---

## 🐳 Docker Deployment

```bash
# Build
docker build -t mindmitra:latest .

# Run
docker run -d -p 8501:8501 --name mindmitra mindmitra:latest
```

Access at `http://localhost:8501`

---

## 🧪 Test Cases

| # | Input | Expected Behavior |
|---|-------|-------------------|
| 1 | "Exams are killing me" | Detects `fear`/`sadness`, shows empathetic response |
| 2 | "I got selected for internship!" | Detects `joy`, energetic response |
| 3 | "I feel like ending it" | **Crisis triggered** — helplines shown, AI response blocked |
| 4 | "Family pressure bahut hai" | Detects `sadness`/`fear`, supportive response |
| 5 | "Feeling okay today" | Detects `neutral`, casual check-in response |
| 6 | Voice button (no mic) | Shows graceful error, app doesn't crash |
| 7 | PDF download | Downloads formatted PDF without unicode crash |
| 8 | Grounding timer | 30-second countdown runs smoothly |

---

## 🔐 Safety & Privacy

- **No data leaves the browser** — everything runs in-session
- **No conversation logging** — session clears on browser close
- **Crisis detection runs first** — before any ML model
- **Verified Indian helplines only** — AASRA, iCall, Vandrevala, Kiran

---

## 🏆 Hackathon Context

Built in **8 hours** at **GNDEC Ludhiana** Hackathon (April 2026).

This is a **prototype** — not a replacement for professional mental health support.
If you or someone you know is struggling, please reach out to the helplines listed in the app.

---

## 👨‍💻 Author

**Sinamor** — B.Tech CSE, GNDEC Ludhiana

---

<p align="center">
  <i>Built with ❤️ for students who need someone to talk to.</i>
</p>
