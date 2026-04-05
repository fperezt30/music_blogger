import os
import requests
from dotenv import load_dotenv

load_dotenv()

WP_URL = os.getenv("WP_URL")  
WP_USER = os.getenv("WP_USER") 
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")  

auth = (WP_USER, WP_APP_PASSWORD)


def create_post(title: str, content: str, artist: str, thumbnail_url: str, status: str = "publish") -> dict:
    """
    Create a WordPress post
    """
    filename = "thumbnail.jpg"
    download_image(thumbnail_url, filename)

    media = upload_media(filename, filename)
    media_id = media["id"]
    category_id = 956

    tag_id = get_or_create_tag(artist)
    
    url = f"{WP_URL}/posts"
    data = {
        "title": title,
        "content": content,
        "status": status,
        "categories": [category_id],
        "tags": [tag_id],
        "featured_media": media_id
    }

    response = requests.post(url, json=data, auth=auth)

    if response.status_code not in (200, 201):
        raise Exception(f"Failed to create post: {response.status_code} - {response.text}")

    return response.json()


def upload_media(file_path: str, filename: str) -> dict:
    """
    Upload media to WordPress
    """
    url = f"{WP_URL}/media"
    headers = {
        "Content-Disposition": f"attachment; filename={filename}"
    }

    with open(file_path, "rb") as f:
        response = requests.post(url, headers=headers, files={"file": f}, auth=auth)

    if response.status_code not in (200, 201):
        raise Exception(f"Failed to upload media: {response.status_code} - {response.text}")

    return response.json()

def update_post(post_id, status):
    url = f"{WP_URL}/posts/{post_id}"

    response = requests.post(
        url,
        json={"status": status},
        auth=auth
    )

    return response.json()

def get_or_create_tag(tag_name):
    # 1. Search for tag
    search_url = f"{WP_URL}/tags?search={tag_name}"
    res = requests.get(search_url, auth=auth)
    tags = res.json()

    if tags:
        return tags[0]["id"]

    # 2. Create tag if not found
    create_res = requests.post(
        f"{WP_URL}/tags",
        json={"name": tag_name},
        auth=auth
    )

    if create_res.status_code not in (200, 201):
        raise Exception(f"Failed to create tag: {create_res.text}")

    return create_res.json()["id"]

def download_image(url, filename):
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Failed to download image")

    with open(filename, "wb") as f:
        f.write(response.content)

    return filename