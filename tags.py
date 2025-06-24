import pandas as pd
import json
from collections import Counter

# Load the Excel file
df = pd.read_excel("keywords-3.xlsx")

# Clean column names
df.columns = df.columns.str.strip()

# Drop NaN and clean keyword strings
keywords = df['keywords'].dropna().astype(str).str.strip()

# Count frequency of each keyword
keyword_freq = Counter(keywords)

# Get top 10 most frequent keywords
top_10_keywords = [kw for kw, _ in keyword_freq.most_common(10)]

# Create tag JSON with ID and Tag fields
tag_json = [{"id": idx + 1, "Tag": tag} for idx, tag in enumerate(top_10_keywords)]

# Save to tags.json
with open("tags.json", "w", encoding="utf-8") as f:
    json.dump(tag_json, f, indent=2, ensure_ascii=False)

print("✅ tags.json created with", len(tag_json), "top keywords by frequency.")
