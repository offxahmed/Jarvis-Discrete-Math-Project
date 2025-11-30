import pyttsx3
from dotenv import load_dotenv
import os

load_dotenv()

def speak(text):
    """Convert text to speech with optimized settings"""
    engine = pyttsx3.init()
    
    # Configure voice properties
    voices = engine.getProperty('voices')
    
    # Set voice (0 = male, 1 = female typically)
    engine.setProperty('voice', voices[0].id)
    
    # Set speaking rate (150-180 for natural speed)
    engine.setProperty('rate', 165)
    
    # Set volume (0.0 to 1.0)
    engine.setProperty('volume', 0.9)
    
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()
