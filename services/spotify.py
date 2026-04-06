import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

load_dotenv()

def get_spotify_client():
    auth_manager = SpotifyClientCredentials(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
    )
    return spotipy.Spotify(auth_manager=auth_manager)

def search_track(sp, artist, song_title):
    query = f"track:{song_title} artist:{artist}"
    results = sp.search(q=query, type="track", limit=1)

    tracks = results.get("tracks", {}).get("items", [])
    
    if not tracks:
        return None
    
    return tracks[0]

def get_artist_genres(sp, artist_id):
    artist = sp.artist(artist_id)
    return artist.get("genres", [])[:2]  

def get_album_label(sp, album_id):
    album = sp.album(album_id)
    return album.get("label", "Not defined")

def fetch_spotify_metadata(artist, song_title):
    sp = get_spotify_client()

    track = search_track(sp, artist, song_title)
    if not track:
        return None

    album_id = track["album"]["id"]
    artist_id = track["artists"][0]["id"]

    label = get_album_label(sp, album_id)
    genres = get_artist_genres(sp, artist_id)

    return {
        "label": label or "Not defined",
        "genres": genres or []
    }