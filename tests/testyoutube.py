from services.youtube import get_youtube_data

if __name__ == "__main__":
    youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    try:
        data = get_youtube_data(youtube_url)

        print("\n✅ YouTube Data Extracted:\n")
        print(f"Video ID: {data['video_id']}")
        print(f"Title: {data['title']}")
        print(f"Author: {data['author']}")
        print(f"Embed URL: {data['embed_url']}")
        print(f"Thumbnail: {data['thumbnail']}")
        print(f"Embed HTML:\n{data['embed_html']}")

    except Exception as e:
        print("\n❌ Error:")
        print(e)