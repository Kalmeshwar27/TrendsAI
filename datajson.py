import pandas as pd
import json
from collections import Counter

# Load Excel
df = pd.read_excel("data-3.xlsx")

# Clean column names
df.columns = df.columns.str.strip()

# Forward-fill 'keywords' to handle merged cells
df['keywords'] = df['keywords'].ffill()

# Drop rows where all key fields are empty
df = df.dropna(subset=["articleTitle", "summary", "overview", "articleLink"], how='all')

# Fill remaining NaNs with empty string
df = df.fillna("")

# Step 1: Count frequency of each keyword
keyword_freq = Counter(df['keywords'])

# Step 2: Get top 10 most common keywords
top_keywords = [kw for kw, _ in keyword_freq.most_common(10)]

# Step 3: Filter dataframe for top keywords only
filtered_df = df[df['keywords'].isin(top_keywords)]

# Step 4: Sort filtered data by keyword frequency (descending)
filtered_df['keyword_rank'] = filtered_df['keywords'].apply(lambda x: top_keywords.index(x))
filtered_df = filtered_df.sort_values(by='keyword_rank')

# Step 5: Build JSON records
records = []
for i, row in filtered_df.iterrows():
    records.append({
        "id": len(records) + 1,
        "keywords": row["keywords"],
        "articleTitle": row["articleTitle"],
        "summary": row["summary"],
        "overview": row["overview"],
        "articleLink": row["articleLink"]
    })

# Step 6: Write JSON file
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2, ensure_ascii=False)

print("✅ JSON file created with top 10 keywords ordered by frequency.")
