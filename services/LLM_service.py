
import os
from dotenv import load_dotenv
import time
from services.spotify import fetch_spotify_metadata
from services.ai_client import generate_with_fallback

load_dotenv()



def data_normalization(title: str, author: str) -> dict:
    """
    Generate blog title and content using Groq.
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
    try:
        response = generate_with_fallback(prompt)
        return response
    except Exception as e:
        print("Error with data normalization:", str(e))
        return {
            "error": True,
            "message": str(e)
        }


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
    try:
        response = generate_with_fallback(prompt)
        return response
    except Exception as e:
        print("Error with Song Metadata Enrichment:", str(e))
        return {
            "error": True,
            "message": str(e)
        }

     
    

def generate_post_content(title, author):

        # Step 1
        step1 = data_normalization(title, author)
        if step1.get("error"):
            return {
                "error": True,
                "message": step1["message"]
            }
        
        print("Step 1 - Data Normalization:", step1)
        
        time.sleep(1.5)  # brief pause to avoid hitting rate limits

        # Step 2
        step2 = enrich_song_metadata(step1["artist"],step1["song_title"])
        if step2.get("error"):
            return {
                "error": True,
                "message": step2["message"]
            }


        print("Step 2 - Song Metadata Enrichment:", step2)

        step3 = fetch_spotify_metadata(step1["artist"],step1["song_title"])
        print("Step 3 - Spotify Metadata:", step3)


        # Merge
        return {
            "title": f"{step1['artist']} - {step1['song_title']} [VIDEO]",
            "tag": step1["artist"],
            "content": f"Country of Origin: {', '.join(step2['country']) if isinstance(step2['country'], list) else step2['country']}\nGenre: {', '.join(step2['genre'])}\nLabel: {step3['label']}"
        }
     