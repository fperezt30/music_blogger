from dotenv import load_dotenv
import os
import json
from google import genai
from services.spotify import fetch_spotify_metadata


load_dotenv()
# Create client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def data_normalization(title: str, author: str) -> dict:
    """
    Generate blog title and content using Gemini (new SDK).
    """

    prompt = f"""
    You are an expert music curator of independent music.
    

    **Task**: Identify the most likely song and artist from input.

    **Input**: 
    title: {title} 
    author: {author}

    Instructions:
    - The input may be noisy, incomplete, or incorrect.
    - Infer the most likely official song.
    - If multiple matches exist, choose the most popular/recognized one.

    Rules:
    - Output MUST be valid JSON
    - No explanations
    - If uncertain, return "Not defined"

    Output format:
    {{
    "artist": "...",
    "song_title": "..."
    }}

    Examples:

    Input: "Blinding Lights", "The Weeknd"
    Output:
    {{
    "artist": "The Weeknd",
    "song_title": "Blinding Lights"
    }}

    Input: "bad guy live", "billie"
    Output:
    {{
    "artist": "Billie Eilish",
    "song_title": "Bad Guy"
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


def enrich_song_metadata(artist: str, song_title: str) -> dict:

   
    prompt = f"""
    You are an expert music curator specializing in independent music.

    Task:
    Provide structured metadata for the given song.

    Input:
    artist: {artist}
    song_title: {song_title}

    Instructions:
    - Use your internal knowledge only
    - Do NOT fabricate information

    Rules:
    - Output MUST be valid JSON
    - No explanations
    - Genre must be a list with max 3 items
    - Country must be max 2 values
    - Label must be a proper noun or "Independent Release" if not found.

    Output format:
    {{
    "country": "...",
    "genre": ["...", "..."],
    "label": "..."
    }}

    Example:

    Input:
    artist: The Weeknd
    song_title: Blinding Lights

    Output:
    {{
    "country": "Canada",
    "genre": ["Synth-pop", "R&B"],
    "label": "Republic Records"
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


def generate_post_content(title, author):

    # Step 1
    step1 = data_normalization(title, author)
    print("Step 1 - Data Normalization:", step1)
    # Step 2
    step2 = enrich_song_metadata(step1["artist"],step1["song_title"])
    print("Step 2 - Song Metadata Enrichment:", step2)
    step3 = fetch_spotify_metadata(step1["artist"],step1["song_title"])
    print("Step 3 - Spotify Metadata:", step3)


    # Merge
    return {
        "title": f"{step1['artist']} - {step1['song_title']} [VIDEO]",
        "content": f"Country of Origin: {', '.join(step2['country']) if isinstance(step2['country'], list) else step2['country']}\nGenre: {', '.join(step2['genre'])}\nLabel:{step3['label']}"
    }