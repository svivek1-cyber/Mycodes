import asyncio
import re
import os
import psutil
import speech_recognition as sr
import pyttsx3
import pyaudio
import time
import webbrowser
import easyocr
import cv2
import pyautogui
import numpy as np
from PIL import ImageGrab
from collections import deque
from datetime import date, datetime
import requests
import tkinter as tk
from tkinter import scrolledtext
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Function to Create Sphere Animation ---
def create_sphere():
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 25)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))
    return x, y, z

# Sphere data
x, y, z = create_sphere()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xticks([]), ax.set_yticks([]), ax.set_zticks([]), ax.grid(False), ax.set_axis_off()
norm = mcolors.Normalize(vmin=z.min(), vmax=z.max())
color_map = cm.rainbow(norm(z))
sphere = ax.plot_surface(x, y, z, facecolors=color_map, rstride=1, cstride=1)

def update(frame):
    ax.view_init(elev=10, azim=frame)

ani = animation.FuncAnimation(fig, update, frames=np.arange(0, 360, 2), interval=50)

# --- GUI Setup ---
root = tk.Tk()
root.title("Mini AI Assistant")
root.geometry("600x500")

label = tk.Label(root, text="Mini AI Assistant", font=("Arial", 18, "bold"))
label.pack()

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

output_text = scrolledtext.ScrolledText(root, height=10, width=70, font=("Arial", 10))
output_text.pack(pady=10)

def update_output_text(text):
    output_text.insert(tk.END, text + "\n")
    output_text.yview(tk.END)

# click_option.py
def capture_live_screen():
    """
    Captures the live screen and returns it as a NumPy array.
    """
    # Capture the live screen
    screenshot = ImageGrab.grab()
    # Convert to a NumPy array for OpenCV processing
    screen_np = np.array(screenshot)
    # Convert from RGB (Pillow format) to BGR (OpenCV format)
    return cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)
def perform_double_click_on_word(screen_img, target_word):
    """
    Detects text in the live screen and performs a double-click on the specified word's location.
    :param screen_img: Live screen capture as a NumPy array.
    :param target_word: The word to search for on the screen.
    """
    # Initialize EasyOCR Reader
    reader = easyocr.Reader(['en'])
    # Perform OCR on the screen image
    results = reader.readtext(screen_img)    
    # Search for the target word and perform a double-click if found
    for (bbox, text, confidence) in results:
        if target_word in text.lower():  # Match the word case-insensitively
            # Extract bounding box coordinates
            (top_left, _, bottom_right, _) = bbox
            x1, y1 = map(int, top_left)
            x2, y2 = map(int, bottom_right)            
            # Calculate the center of the bounding box
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2            
            print(f"Target word '{text}' found at ({center_x}, {center_y}). Confidence: {confidence:.2f}")            
            # Simulate a double-click at the center of the bounding box
            pyautogui.moveTo(center_x, center_y)
            pyautogui.doubleClick()  # Perform a double-click
            return
    print(f"Word '{target_word}' not found on the screen.")    

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

# --- AI Assistant API ---
def mini_ai_assistant(command):
    API_KEY = "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"
    API_URL = "https://api.groq.com/openai/v1/chat/completions"

    conversation_history = [{"role": "system", "content": "You are Mini AI, a helpful assistant."}]
    def ask_question(question):
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        conversation_history.append({"role": "user", "content": question})
        payload = {"model": "llama-3.3-70b-versatile", "messages": conversation_history}
        response = requests.post(API_URL, json=payload, headers=headers)

        if response.status_code == 200:
            answer = response.json()["choices"][0]["message"]["content"]
            conversation_history.append({"role": "assistant", "content": answer})
            return answer
        else:
            return f"Error: {response.status_code}, {response.text}"

    formatted_input = f"suppose you are Mini, my AI assistant\nThe question is:\n{command}\nAnswer in short and easy language.when you need listing, Don't answer using * on the behalf of this you can use 1st, 2nd and so no."
    response = ask_question(formatted_input)
    update_output_text("Answer: " + response)
    speak(response)
# app_control.py

app_commands = {
    "notepad": ("notepad", "notepad.exe"),
    "calculator": ("calc", "Calculator.exe"),
    "chrome": (r'"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"', "chrome.exe"),
    "command prompt": ("cmd", "cmd.exe"),
    "vs code": ("code", "Code.exe"),
    "whatsapp": ("start whatsapp", "WhatsApp.exe"),
    "ms edge": (r'"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"', "msedge.exe"),
    "file explorer": (r'"C:\\Windows\\explorer.exe"',"explorer.exe")
}

def open_app(app_name):
    if app_name in app_commands:
        command, _ = app_commands[app_name]
        speak(f"Opening {app_name}")
        print(f"mini said: Opening {app_name}")
        os.system(command)
    else:
        speak(f"Sorry, I couldn't find {app_name} on this system.")
        print(f"mini said: Sorry, I couldn't find {app_name} on this system.")

def close_app(app_name):
    if app_name in app_commands:
        _, process_name = app_commands[app_name]
        found_process = False

        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'].lower() == process_name.lower():
                found_process = True
                speak(f"Closing {app_name}")
                print(f"Mini said: Closing {app_name}")

                try:
                    proc.terminate()  # Attempt to gracefully shut down
                    proc.wait(timeout=3)  # Wait for it to close
                    speak(f"{app_name} has been closed.")
                    print(f"Mini said: {app_name} has been closed.")
                except psutil.NoSuchProcess:
                    print(f"{app_name} has already terminated.")
                except psutil.TimeoutExpired:
                    proc.kill()  # Force kill if it doesn't terminate
                    speak(f"{app_name} had to be forcefully closed.")
                    print(f"Mini said: {app_name} had to be forcefully closed.")
        
        if not found_process:
            speak(f"{app_name} is not currently running.")
            print(f"Mini said: {app_name} is not currently running.")
    else:
        speak(f"Sorry, I couldn't find {app_name} on this system.")
        print(f"Mini said: Sorry, I couldn't find {app_name} on this system.")

# utilities.py

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
 

# --- Command Handling ---
def handle_command(command):
    exit_commands = ["exit", "stop", "quit", "bye"]
    for exit_command in exit_commands:
        if exit_command in command:
            speak(f"Ok, {exit_command}")
            print(f"Mini said: OK {exit_command}")
            root.destroy()  # Close the GUI
            exit()  # Exit the program
    if "time" in command :
        get_time()
    elif  "date" in command:
        get_date()
    elif "search" in command:
        search_query = command.replace("search for", "").strip()
        search_google(search_query)
    elif "open" in command:
        app_name = command.replace("open", "").strip()
        open_app(app_name)
    elif "close" in command:
        app_name = command.replace("close", "").strip()
        close_app(app_name)
    elif "click on" in command:
        target_word = command.replace("click on", "").strip()
        if not target_word:
            print("No valid voice command detected.")
            return
        print("Capturing live screen...")
        # Capture the live screen
        live_screen = capture_live_screen()

        # Perform double-click action on the detected word
        perform_double_click_on_word(live_screen, target_word)
       
    elif "stay" in command:
        match = re.search(r"stay for (\d+) minutes", command)
        if match:
            t = int(match.group(1)) * 60
            time.sleep(t)
    
    elif "write" in command or "right" in command:
        text = command.replace("write", "").replace("right", "").strip()
        speak(f"Writing: {text}")
        with open("text.txt", "w") as f:
            # Replace both "write" and "right" if they exist in the command
            f.write(text)
        speak("Your text has been written to the file .")
    else:
        # Handover command to handle by AI
        mini_ai_assistant(command)

# --- Continuous Listening Function ---
def start_continuous_listening():
    def listen_loop():
        while True:
            command = get_audio()
            handle_command(command)

    threading.Thread(target=listen_loop, daemon=True).start()

# --- Start Button ---
def start_app():
    greeting = greet()
    speak(f"Welcome, {greeting}")
    speak("I'm Mini. How can I help you?")
    start_continuous_listening()

start_button = tk.Button(root, text="Start", font=("Arial", 12), command=start_app)
start_button.pack(pady=10)

# --- Exit Button ---
def exit_app():
    root.destroy()
    exit()

exit_button = tk.Button(root, text="Exit", font=("Arial", 12), command=exit_app)
exit_button.pack(pady=10)

# --- Greet User ---
def greet():
    current_hour = datetime.now().hour
    if 4 <= current_hour < 12:
        return "Good morning!"
    elif 12 <= current_hour < 16:
        return "Good afternoon!"
    elif 16 <= current_hour <= 20:
        return "Good evening!"
    else:
        return "It's your working time"

# --- Start the App ---
if __name__ == "__main__":
    root.mainloop()
