from flask import Flask, request, jsonify, render_template
from services import wordpress
from services.youtube import get_youtube_data
from services.gemini_service import generate_post_content
from services.wordpress import create_post,update_post


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


def build_embed(embed_url: str) -> str:
    return f"""
    <iframe width="560" height="315"
    src="{embed_url}"
    frameborder="0"
    allowfullscreen></iframe>
    """


@app.route("/create-post", methods=["POST"])
def create_post_from_url():
    try:
        data = request.json
        youtube_url = data.get("url")

        if not youtube_url:
            return jsonify({"error": "Missing URL"}), 400

        # 1. YouTube
        yt_data = get_youtube_data(youtube_url)

        # 2. Gemini
        ai_content = generate_post_content(
            yt_data["title"],
            yt_data["author"]
        )

        # 3. Build content
        final_content = f"""
        {ai_content['content']}
        <br><br>
        {build_embed(yt_data['embed_url'])}
        """

        # 4. Publish a post
        post = create_post(
            title=ai_content["title"],
            content=final_content,
            artist = yt_data["author"],
            thumbnail_url = yt_data["thumbnail"],
            status="publish"
        )

        return jsonify({
            "status": "Published",
            "post_id": post["id"],
            "publish_link": post.get("link")
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/update-post-status", methods=["POST"])
def update_post_status():
    try:
        data = request.json
        post = wordpress.update_post(
            post_id=data["post_id"],
            status=data["status"]
        )

        return jsonify({
            "status": "Draft",
            "new_status": post.get("status"),
            "link": post.get("link")
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)