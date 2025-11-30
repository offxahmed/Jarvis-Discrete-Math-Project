import cohere
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize Cohere client
co = cohere.Client(os.getenv("COHERE_API_KEY"))

# Define decision categories
FUNCTIONS = [
    "general",      # Normal conversation
    "real_time",    # Internet search needed
    "automation",   # System/app control
    "open",         # Open applications
    "close",        # Close applications
    "search",       # YouTube/Web search
    "generate_image", # AI image generation
    "content",      # Write emails/letters
    "exit"          # End conversation
]

SYSTEM_PROMPT = """
You are a decision-making AI for JARVIS assistant. Analyze user queries and classify them:

**GENERAL:** Questions answerable without real-time data (e.g., "How are you?", "What is photosynthesis?")
**REAL_TIME:** Requires internet search (e.g., "Tesla stock price", "Who is Elon Musk", "Latest news")
**AUTOMATION:** System controls (e.g., "mute PC", "increase volume", "lock screen")
**OPEN:** Launch apps (e.g., "open YouTube", "open Chrome", "open Spotify")
**CLOSE:** Close apps (e.g., "close Chrome", "close Notepad")
**SEARCH:** Search queries (e.g., "search Python tutorial on YouTube", "search latest AI news")
**GENERATE_IMAGE:** Image creation (e.g., "generate image of a dog", "create a sunset picture")
**CONTENT:** Writing tasks (e.g., "write email to principal", "compose letter")
**EXIT:** End conversation (e.g., "goodbye", "bye Jarvis", "exit")

Respond ONLY with: [CATEGORY] [original query]
Example: "real_time What is Tesla stock price"
"""

def decide_query_type(query):
    """Use LLM to classify query type"""
    response = co.chat(
        model="command-r-plus",
        message=f"{SYSTEM_PROMPT}\n\nUser Query: {query}",
        temperature=0.3
    )
    
    decision = response.text.strip()
    
    # Parse decision
    for func in FUNCTIONS:
        if decision.lower().startswith(func):
            return func, query
    
    return "general", query  # Default fallback
