
# build_cwe_retriever.py
# Builds a TF-IDF search index over CWE CSVs to suggest related weaknesses & mitigations.
import os, joblib, pandas as pd, numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

CSV_FILES = ["./data/699.csv", "./data/1194.csv"]  # uploaded
TEXT_FIELDS = ["CWE-ID","Name","Description","Extended Description","Modes Of Introduction","Exploitation Factors","Common Consequences","Detection Methods","Potential Mitigations","Notes"]

def load_cwe(csvs):
    frames = []
    for p in csvs:
        if os.path.exists(p):
            frames.append(pd.read_csv(p, low_memory=False))
    if not frames:
        raise SystemExit("No CWE CSVs found.")
    df = pd.concat(frames, ignore_index=True)
    # Build a single text field
    def row_text(r):
        parts = []
        for f in TEXT_FIELDS:
            if f in r and pd.notna(r[f]):
                parts.append(str(r[f]))
        return " ".join(parts)
    df["_text"] = df.apply(row_text, axis=1)
    df["_title"] = df["Name"] if "Name" in df.columns else df.get("CWE-ID","CWE")
    return df

df = load_cwe(CSV_FILES)

vec = TfidfVectorizer(ngram_range=(1,2), min_df=2, max_df=0.95, sublinear_tf=True)
X = vec.fit_transform(df["_text"].fillna(""))
nn = NearestNeighbors(n_neighbors=5, metric="cosine").fit(X)

os.makedirs("darksecai_models", exist_ok=True)
df_small = df[["CWE-ID","Name","Potential Mitigations","Description","Notes"]].copy() if "CWE-ID" in df.columns else df.copy()
joblib.dump({"vectorizer": vec, "nn": nn, "texts": df["_text"].tolist(), "meta": df_small}, "darksecai_models/cwe_retriever.joblib")
print("Saved -> darksecai_models/cwe_retriever.joblib (kNN over CWE texts)")
