from services.youtube import get_youtube_data
from services.gemini_service import generate_post_content
from services.wordpress import create_post


def build_embed(embed_url: str) -> str:
    return f"""
    <iframe width="560" height="315"
    src="{embed_url}"
    frameborder="0"
    allowfullscreen></iframe>
    """


def publish_from_youtube(url: str):
    # 1. Extract YouTube data
    yt_data = get_youtube_data(url)

    title = yt_data["title"]
    artist = yt_data["author"]
    embed_url = yt_data["embed_url"]

    # 2. Generate content with Gemini
    ai_content = generate_post_content(title, artist)

    blog_title = ai_content["title"]
    blog_content = ai_content["content"]

    # 3. Add YouTube embed
    final_content = f"""
    {blog_content}
    <br><br>
    {build_embed(embed_url)}
    """

    # 4. Publish to WordPress
    post = create_post(
        title=blog_title,
        content=final_content
    )

    print("\n✅ Post created!")
    print("ID:", post["id"])
    print("Link:", post.get("link"))


if __name__ == "__main__":
    youtube_url = input("Enter YouTube URL: ")
    publish_from_youtube(youtube_url)