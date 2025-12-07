import cohere
from dotenv import load_dotenv
import os

load_dotenv()

# Determine the directory where .env should be (e.g., project root)
# This assumes model.py is in backend/ and .env is in the parent directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, '.env')
load_dotenv(ENV_PATH)

api_key = os.getenv("COHERE_API_KEY")

# Check for missing or placeholder API key
if not api_key or api_key.strip() == "your_cohere_api_key_here":
    print("\n" + "!" * 80)
    print("CRITICAL ERROR: Missing Cohere API Key!")
    print(f"Please open the file: {ENV_PATH}")
    print("And replace 'your_cohere_api_key_here' with your actual Cohere API key.")
    print("You can get a free key from: https://dashboard.cohere.com/api-keys")
    print("!" * 80 + "\n")
    # Prevent crash by using a dummy key for now, but warned user.
    # The API call will still fail 401 if we proceed, so best to exit or handle gracefully.
    # We will let it fail later or we can raise a SystemExit here.
    # Let's raise SystemExit to stop the loop clearly.
    raise SystemExit("Exiting due to missing API configuration.")

# Initialize Cohere client
co = cohere.Client(api_key)

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
