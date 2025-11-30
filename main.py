import threading
from backend.speech_to_text import listen
from backend.text_to_speech import speak
from backend.model import decide_query_type
from backend.chatbot import chat
from backend.real_time_search_engine import real_time_search
from backend.automation import *
from backend.image_generation import generate_image

def jarvis_brain(query):
    """Process query through decision-making system"""
    
    # Classify query type
    decision, processed_query = decide_query_type(query)
    
    response = ""
    
    # Route to appropriate handler
    if decision == "general":
        response = chat(processed_query)
    
    elif decision == "real_time":
        response = real_time_search(processed_query)
    
    elif decision == "open":
        app_name = processed_query.replace("open", "").strip()
        response = open_application(app_name)
    
    elif decision == "close":
        app_name = processed_query.replace("close", "").strip()
        response = close_application(app_name)
    
    elif decision == "search":
        query_text = processed_query.replace("search", "").strip()
        response = youtube_search(query_text)
    
    elif decision == "automation":
        response = system_control(processed_query)
    
    elif decision == "generate_image":
        prompt = processed_query.replace("generate image", "").strip()
        response = generate_image(prompt)
    
    elif decision == "exit":
        response = "Goodbye, Sir. Have a great day!"
        speak(response)
        exit()
    
    else:
        response = "I didn't understand that command."
    
    return response

def main():
    """Main execution loop"""
    speak("Initializing Jarvis System...")
    speak("Good evening, Sir. I am Jarvis. How may I help you?")
    
    while True:
        # Listen for wake word or command
        query = listen()
        
        if query:
            # Process through brain
            response = jarvis_brain(query)
            
            # Speak response
            speak(response)

if __name__ == "__main__":
    main()
