# Manav — Graceful Voice Fallback implementation
# Handles cases where PyAudio is missing, missing mics, or timeouts seamlessly.

import speech_recognition as sr
import pyttsx3

def speech_to_text() -> str:
    """
    Listens to microphone & uses Google Web Speech API.
    Returns graceful error string instead of crashing Streamlit if hardware fails.
    """
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.7)
            # Short timeout so the app doesn't hang forever
            audio = r.listen(source, timeout=6)
        
        text = r.recognize_google(audio)
        return text
    
    except sr.WaitTimeoutError:
        return "Error: Timeout — it was too quiet. Try again."
    except sr.UnknownValueError:
        return "Error: Could not understand audio. Try speaking clearer."
    except Exception as e:
        # Most likely PyAudio not installed or no mic plugged in
        return f"Error: Hardware or dependency issue. Did you pip install PyAudio? ({str(e)[:50]})"

def text_to_speech(text: str):
    """
    Local testing function for text-to-speech.
    We don't block failures here so it doesn't crash cloud deployments (cloud servers have no speakers).
    """
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass  # Completely silent failure for Streamlit Cloud
