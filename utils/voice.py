# Sinamor
import speech_recognition as sr
import pyttsx3

def speech_to_text():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source, timeout=5)
        return r.recognize_google(audio)
    except Exception as e:
        return f"Error: Could not access microphone or recognize speech. ({e})"

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
