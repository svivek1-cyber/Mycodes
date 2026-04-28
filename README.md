# Mini AI Assistant

A minimal AI assistant built with Python that provides speech recognition, text-to-speech, optical character recognition (OCR) for screen interaction, and a graphical user interface (GUI) featuring a 3D animated sphere.

## Features

- **Speech Recognition**: Listen to voice commands using speech_recognition.
- **Text-to-Speech**: Respond with synthesized speech using pyttsx3.
- **Screen OCR**: Capture live screen and detect text using EasyOCR.
- **Automated Interaction**: Perform double-clicks on detected words on the screen.
- **GUI Interface**: Tkinter-based interface with a 3D rotating sphere animation powered by Matplotlib.
- **System Monitoring**: Utilizes psutil for system information.
- **Web Integration**: Open URLs with webbrowser.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/svivek1-cyber/Mycodes.git
   cd Mycodes
   ```

2. Install the required dependencies:
   ```
   pip install speechrecognition pyttsx3 pyaudio easyocr opencv-python pyautogui pillow psutil requests matplotlib
   ```

   Note: For pyaudio, you may need to install system dependencies:
   - On Ubuntu/Debian: `sudo apt-get install portaudio19-dev`
   - On macOS: `brew install portaudio`

3. Ensure you have Python 3.7+ installed.

## Usage

Run the application:
```
python mini.py
```

The GUI will launch with the animated sphere. Use the interface to interact with the assistant. Voice commands can be processed, and screen text can be analyzed for automated clicks.

## Requirements

- Python 3.7+
- Microphone for speech recognition
- Webcam/screen capture permissions for OCR

## Contributing

Feel free to submit issues and pull requests.

## License

This project is open-source. See LICENSE file for details.