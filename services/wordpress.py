import os
import requests
from dotenv import load_dotenv

load_dotenv()

WP_URL = os.getenv("WP_URL")  
WP_USER = os.getenv("WP_USER") 
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")  

auth = (WP_USER, WP_APP_PASSWORD)


def create_post(title: str, content: str, status: str = "publish") -> dict:
    """
    Create a WordPress post
    """
    url = f"{WP_URL}/posts"
    data = {
        "title": title,
        "content": content,
        "status": status
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