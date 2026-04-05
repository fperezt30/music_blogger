import requests
from urllib.parse import urlparse, parse_qs


def extract_video_id(youtube_url: str) -> str:
    """
    Extract YouTube video ID from a URL.
    """
    parsed_url = urlparse(youtube_url)

    if parsed_url.hostname in ["youtu.be"]:
        return parsed_url.path[1:]

    if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        if parsed_url.path == "/watch":
            return parse_qs(parsed_url.query).get("v", [None])[0]
        elif parsed_url.path.startswith("/embed/"):
            return parsed_url.path.split("/")[2]

    return None


def get_embed_url(video_id: str) -> str:
    """
    Return embeddable YouTube URL.
    """
    return f"https://www.youtube.com/embed/{video_id}"


def get_video_metadata(video_id: str) -> dict:
    """
    Fetch video metadata using YouTube oEmbed (no API key required).
    """
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch metadata: {response.text}")

    data = response.json()

    return {
        "title": data.get("title"),
        "author": data.get("author_name"),  # usually channel / artist
        "thumbnail": data.get("thumbnail_url"),
        "html": data.get("html")  # contains embed iframe
    }


def get_youtube_data(youtube_url: str) -> dict:
    """
    Main function: takes a URL and returns structured data.
    """
    video_id = extract_video_id(youtube_url)

    if not video_id:
        raise ValueError("Invalid YouTube URL")

    metadata = get_video_metadata(video_id)
    thumbnail = get_best_thumbnail(video_id)

    return {
        "video_id": video_id,
        "title": metadata["title"],
        "author": metadata["author"],
        "embed_url": get_embed_url(video_id),
        "thumbnail": thumbnail,
        "embed_html": metadata["html"]
    }

def get_best_thumbnail(video_id):
    urls = [
        f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
        f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
    ]

    for url in urls:
        res = requests.head(url)
        if res.status_code == 200:
            return url

    return urls[-1]