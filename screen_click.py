import easyocr
import cv2
import pyautogui
import numpy as np
from PIL import ImageGrab

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