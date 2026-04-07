# Sinamor — voice module
# Graceful fallback: if no mic or PyAudio, app doesn't crash

import speech_recognition as sr
import pyttsx3


def speech_to_text() -> str:
    """
    Listens via microphone and returns transcribed text.
    Returns an Error string (not exception) if hardware is missing.
    """
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        return recognizer.recognize_google(audio)
    except sr.WaitTimeoutError:
        return "Error: Timed out — no speech detected."
    except sr.UnknownValueError:
        return "Error: Couldn't understand the audio. Try again."
    except Exception as e:
        # Sinamor: this catches missing PyAudio, no mic hardware, etc.
        return f"Error: Mic/PyAudio issue — {str(e)[:60]}"


def text_to_speech(text: str):
    """Local TTS for developer testing. Non-blocking on failure."""
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass  # silently skip on cloud where no audio device exists
