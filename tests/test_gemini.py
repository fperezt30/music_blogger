from services.gemini_service import generate_post_content

if __name__ == "__main__":
    result = generate_post_content(
        title="Midnight City",
        artist="M83"
    )

    print("\n✅ Generated Content:\n")
    print(result)