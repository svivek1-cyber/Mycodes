import os
import psutil
from speech import speak

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