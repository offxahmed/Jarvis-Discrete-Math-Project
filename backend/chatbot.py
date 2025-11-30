from groq import Groq
from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

USER_NAME = os.getenv("USER_NAME", "Sir")
ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "Jarvis")

# Chat history storage
CHAT_LOG = "frontend/files/database.json"

SYSTEM_PROMPT = f"""You are {ASSISTANT_NAME}, an advanced AI assistant similar to JARVIS from Iron Man. 
You assist {USER_NAME} with tasks, answer questions accurately, and maintain a professional yet friendly tone.
- Be concise but informative
- Don't mention current time unless asked
- You have access to real-time information
- Current date: {datetime.now().strftime('%B %d, %Y')}"""

def load_chat_history():
    """Load previous conversations"""
    try:
        with open(CHAT_LOG, 'r') as f:
            return json.load(f)
    except:
        return []

def save_chat_history(messages):
    """Save conversation history"""
    with open(CHAT_LOG, 'w') as f:
        json.dump(messages, f, indent=2)

def chat(query):
    """Generate response using Groq Llama"""
    messages = load_chat_history()
    
    # Add system prompt if first message
    if not messages:
        messages.append({"role": "system", "content": SYSTEM_PROMPT})
    
    # Add user query
    messages.append({"role": "user", "content": query})
    
    # Get response from Groq
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Fast and accurate
        messages=messages,
        temperature=0.7,
        max_tokens=500
    )
    
    answer = response.choices[0].message.content
    
    # Add assistant response to history
    messages.append({"role": "assistant", "content": answer})
    
    # Save updated history
    save_chat_history(messages)
    
    return answer
