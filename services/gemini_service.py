from dotenv import load_dotenv
import os
import json
from google import genai

load_dotenv()
# Create client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    
def generate_post_content(title: str, artist: str) -> dict:
    """
    Generate blog title and content using Gemini (new SDK).
    """

    prompt = f"""
    You are a music blogger.

    Based on the following song:
    Title: {title}
    Artist: {artist}

    Generate:
    1. A catchy blog post title
    2. A short blog post (2–3 paragraphs)

    Respond ONLY in JSON format like:
    {{
        "title": "...",
        "content": "..."
    }}
    """

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    output_text = response.text.strip()

    # Clean markdown if present
    if output_text.startswith("```"):
        output_text = output_text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(output_text)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON from Gemini:\n{output_text}")