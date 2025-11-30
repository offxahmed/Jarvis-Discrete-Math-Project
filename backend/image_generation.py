import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_image(prompt):
    """Generate image using DALL-E"""
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        
        image_url = response['data'][0]['url']
        return f"Image generated: {image_url}"
    except Exception as e:
        return f"Image generation failed: {str(e)}"
