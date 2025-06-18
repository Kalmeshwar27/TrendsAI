from flask import Flask, jsonify
import json
from flask import Response
app = Flask(__name__)

# Load data files once at startup
try:
    with open("tags.json", encoding="utf-8") as f:
        tags_data = json.load(f)

    with open("data.json", encoding="utf-8") as f:
        article_data = json.load(f)

    print("✅ JSON files loaded successfully.")

except Exception as e:
    print("❌ Error loading JSON files:", e)
    tags_data = []
    article_data = []

# Map ID to Tag name from tags.json
id_to_tag = {tag["id"]: tag["Tag"] for tag in tags_data if "id" in tag and "Tag" in tag}

# Root route to verify server is live
@app.route("/")
def home():
    return "✅ Flask API is running. Use /tags, /data, or /tag/<tag_name>"

# Get all tags
@app.route("/tags", methods=["GET"])
def get_tags():
    return Response(json.dumps(tags_data, indent=2), mimetype="application/json")

# Get all articles
@app.route("/data", methods=["GET"])
def get_all_data():
    return jsonify(article_data)

# Get articles by tag name (Verb Phrase)
@app.route("/tag/<tag_name>", methods=["GET"])
def get_articles_by_tag(tag_name):
    filtered = [
        article for article in article_data
        if article.get("Verb Phrase", "").lower() == tag_name.lower()
    ]
    if not filtered:
        return jsonify({"message": f"No articles found for tag '{tag_name}'"}), 404
    return jsonify(filtered)

# Get articles by tag ID
@app.route("/tag/id/<int:tag_id>", methods=["GET"])
def get_articles_by_tag_id(tag_id):
    tag_name = id_to_tag.get(tag_id)
    if not tag_name:
        return jsonify({"message": f"No tag found with ID {tag_id}"}), 404
    return get_articles_by_tag(tag_name)

# Run the app
# Run the app
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

