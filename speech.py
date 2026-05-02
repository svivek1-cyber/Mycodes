import speech_recognition as sr
import pyttsx3
from collections import deque
from gui import update_output_text

# --- Text-to-Speech Function ---
def speak(text):
    engine = pyttsx3.init()
    voice = engine.getProperty('voices')
    engine.setProperty('voice', voice[1].id)
    engine.say(text)
    engine.runAndWait()

# --- Speech Recognition Function ---
queue = deque(maxlen=2)

def get_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        update_output_text("Listening...")
        audio = recognizer.listen(source)
        command = ""
        try:
            command = recognizer.recognize_google(audio).lower()
            queue.append(command)
            update_output_text(f"You said: {command}")
        except sr.UnknownValueError:
            update_output_text("Sorry, I couldn't understand. Please say something...")
        except sr.RequestError:
            update_output_text("There seems to be an issue with the internet connection.")
    return command