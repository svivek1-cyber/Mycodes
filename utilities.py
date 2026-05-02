import time
import webbrowser
from datetime import date
from speech import speak

def get_time():
    current_time = time.strftime("%I:%M %p")
    speak(f"Current time is {current_time}")
    
def get_date():
    current_date = date.today().strftime('%m-%d-%Y')  # Example: DD-MM-YYYY
    speak(f"todays date is {current_date}")

def search_google(query): 
    if query:
        speak(f"Searching for {query} on Google.")
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
    else:
        speak("Please specify what you want to search for.")