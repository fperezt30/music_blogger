from dotenv import load_dotenv
import os
import json
from google import genai

load_dotenv()
# Create client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    
def generate_post_content(title: str, author: str) -> dict:
    """
    Generate blog title and content using Gemini (new SDK).
    """

    prompt = f"""
    You are a seasoned music blogger who has been writing about independent music for more than a decade.
    You have a deep interest in niche genres and emerging artists around the world.

    Based on the following song:
    Title: {title}
    Author: {author}

    Generate:
    1. A title that includes the following format: Name of the artist - "Title of the song" [VIDEO]
    2. A bullet list that includes relevant data from the artist. The critical information that you should include in the bullet list is:
    -Country of origin (you will find this information on the artist's website or social media, but if not available, you can try to find it on music platforms like Spotify or Bandcamp).
    -Genre (you can find this information on the artist's website, social media, or music platforms like Spotify or Bandcamp).
    -Label: you will go to the artist's website and find the name of the label that released the song. If you can't find it, you can mention that it's an independent release.

    Remember: 
    1. No need to write a paragraph, just a bullet list with the most relevant information about the artist and the song.
    2. In the majority of scenarios, {title} will contain the name of the song, and {author} will contain the name of the artist. 
    2. Sometimes the name of the label is included in the {author} field, and the name of the artists is included in the {title}. If you're not sure, make a decision based on the information you just previously searched about the artist and the song.

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