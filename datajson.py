import pandas as pd
import json

# Load Excel
df = pd.read_excel("data-2.xlsx")

# Clean column names
df.columns = df.columns.str.strip()

# Forward-fill 'Verb Phrase' to handle merged cells
df['Keywords'] = df['Keywords'].ffill()

# Drop rows where all key fields are empty
df = df.dropna(subset=["Article Title", "Summary", "Overview", "Article Link"], how='all')

# Fill remaining NaNs with empty string
df = df.fillna("")

# Create JSON records with Verb Phrase included
records = []
for i, row in df.iterrows():
    records.append({
        "id": i + 1,
        "Keywords": row.get("Keywords", ""),
        "ArticleTitle": row.get("Article Title", ""),
        "Summary": row.get("Summary", ""),
        "Overview": row.get("Overview", ""),
        "Article Link": row.get("Article Link", "")
    })

# Write JSON file
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2, ensure_ascii=False)

print("✅ JSON file created with Verb Phrase included.")
