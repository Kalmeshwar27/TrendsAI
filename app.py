from flask import Flask, jsonify, Response
from flask_cors import CORS
import json
from collections import Counter

app = Flask(__name__)
CORS(app)  # ✅ allow all origins

# Load and process data files once at startup
try:
    with open("data.json", encoding="utf-8") as f:
        all_articles = json.load(f)

    # Count frequency of each keyword
    keyword_list = [a.get("keywords", "").strip() for a in all_articles if a.get("keywords")]
    keyword_freq = Counter(keyword_list)

    # Get top 10 keywords by frequency
    top_keywords = [kw for kw, _ in keyword_freq.most_common(10)]

    # Filter articles to include only those with top keywords
    article_data = [
        article for article in all_articles
        if article.get("keywords", "").strip() in top_keywords
    ]

    # Sort articles by keyword frequency order
    keyword_rank = {kw: i for i, kw in enumerate(top_keywords)}
    article_data.sort(key=lambda x: keyword_rank.get(x.get("keywords", "").strip(), float("inf")))

    # Generate tags_data from top keywords
    tags_data = [{"id": i + 1, "Tag": kw} for i, kw in enumerate(top_keywords)]

    # Map ID to Tag
    id_to_tag = {tag["id"]: tag["Tag"] for tag in tags_data}

    print("✅ JSON files loaded and processed by frequency.")

except Exception as e:
    print("❌ Error loading JSON files:", e)
    tags_data = []
    article_data = []
    id_to_tag = {}

@app.route("/")
def home():
    return "✅ Flask API is running. Use /tags, /data, or /tag/<tag_name>"

@app.route("/tags", methods=["GET"])
def get_tags():
    return Response(json.dumps(tags_data, indent=2), mimetype="application/json")

@app.route("/data", methods=["GET"])
def get_all_data():
    return jsonify(article_data)

@app.route("/tag/<tag_name>", methods=["GET"])
def get_articles_by_tag(tag_name):
    filtered = [
        article for article in article_data
        if article.get("keywords", "").strip().lower() == tag_name.lower()
    ]
    if not filtered:
        return jsonify({"message": f"No articles found for tag '{tag_name}'"}), 404
    return jsonify(filtered)

@app.route("/tag/id/<int:tag_id>", methods=["GET"])
def get_articles_by_tag_id(tag_id):
    tag_name = id_to_tag.get(tag_id)
    if not tag_name:
        return jsonify({"message": f"No tag found with ID {tag_id}"}), 404
    return get_articles_by_tag(tag_name)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
