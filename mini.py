import re
import time
import tkinter as tk
import threading

from gui import root, update_output_text, greet
from speech import speak, get_audio
from app_control import open_app, close_app
from utilities import get_time, get_date, search_google
from screen_click import capture_live_screen, perform_double_click_on_word
from ai_assistant import mini_ai_assistant

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

# --- Start the App ---
if __name__ == "__main__":
    root.mainloop()
