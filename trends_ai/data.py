import pandas as pd
import json

# Load Excel
df = pd.read_excel("data-1.xlsx")

# Clean column names
df.columns = df.columns.str.strip()

# Forward-fill 'Verb Phrase' to handle merged cells (not needed anymore, but harmless)
df['Verb Phrase'] = df['Verb Phrase'].ffill()

# Drop rows where all key fields are empty
df = df.dropna(subset=["Article Title", "Summary", "Overview", "Article Link"], how='all')

# Fill remaining NaNs with empty string
df = df.fillna("")

# Create JSON records with only required fields in the desired order
records = []
for i, row in df.iterrows():
    records.append({
        "id": i + 1,
        "ArticleTitle": row.get("Article Title", ""),
        "Overview": row.get("Overview", ""),
        "Summary": row.get("Summary", ""),
        "Article Link": row.get("Article Link", "")
    })

# Write JSON file
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2, ensure_ascii=False)

print("✅ JSON file created in the required format.")
