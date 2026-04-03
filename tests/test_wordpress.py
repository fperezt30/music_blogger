from services.wordpress import create_post

if __name__ == "__main__":
    post = create_post(
        title="Test Post from Agent",
        content="<p>This is a test post</p>"
    )
    print("Post created! ID:", post["id"])