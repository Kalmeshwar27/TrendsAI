import pandas as pd
import json

# Load the Excel file
df = pd.read_excel("Trendsfeed(Keywords)-1.xlsx")

# Extract unique verb phrases
unique_tags = df['Keywords'].dropna().unique()

# Create JSON with IDs
tag_json = [{"id": idx + 1, "Tag": tag} for idx, tag in enumerate(sorted(unique_tags))]

# Save to tags.json
with open("tags.json", "w") as f:
    json.dump(tag_json, f, indent=2)

print("✅ tags.json created with", len(tag_json), "tags.")
