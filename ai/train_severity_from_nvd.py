
# train_severity_from_nvd.py
# Trains a text classifier on NVD JSON (nvdcve-2.0-*.json) to predict CVSS severity.
import os, json, re, joblib, numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from xgboost import XGBClassifier

NVD_FILES = [
    "./data/nvdcve-2.0-recent.json",
    "./data/nvdcve-2.0-modified.json"
]

def load_items(paths):
    rows = []
    for p in paths:
        if not os.path.exists(p):
            continue
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        for v in data.get("vulnerabilities", []):
            c = v.get("cve", {})
            descs = c.get("descriptions", [])
            text = ""
            if descs:
                # prefer English
                for d in descs:
                    if d.get("lang","en").lower() == "en":
                        text = d.get("value","")
                        break
                if not text:
                    text = descs[0].get("value","")
            sev = None
            m = c.get("metrics", {})
            for k in ["cvssMetricV31","cvssMetricV30"]:
                if m.get(k):
                    sev = m[k][0].get("cvssData", {}).get("baseSeverity")
                    if sev: break
            if not sev and m.get("cvssMetricV2"):
                sev = m["cvssMetricV2"][0].get("baseSeverity")
                # Normalize to v3 buckets (map 'MEDIUM','HIGH','LOW')
                if sev and sev.upper() == "MEDIUM": sev = "MEDIUM"
            if text and sev:
                rows.append((text, sev.upper()))
    return rows

data = load_items(NVD_FILES)
texts, labels = zip(*data) if data else ([], [])
print("Loaded NVD items:", len(texts))

# Train/test split
le = LabelEncoder()
y = le.fit_transform(labels)
Xtr_texts, Xva_texts, ytr, yva = train_test_split(texts, y, test_size=0.2, random_state=42, stratify=y)

# TF-IDF + XGBoost multiclass
tfidf = TfidfVectorizer(ngram_range=(1,2), min_df=3, max_df=0.9, sublinear_tf=True)
Xtr = tfidf.fit_transform(Xtr_texts)
Xva = tfidf.transform(Xva_texts)

xgb = XGBClassifier(
    objective="multi:softprob",
    num_class=len(le.classes_),
    n_estimators=600, max_depth=6, learning_rate=0.08,
    subsample=0.9, colsample_bytree=0.9, reg_lambda=1.0, tree_method="hist",
    random_state=42, n_jobs=0,
)
xgb.fit(Xtr, ytr, eval_set=[(Xva, yva)], verbose=False)

yhat = xgb.predict(Xva)
print(classification_report(yva, yhat, target_names=le.classes_))

os.makedirs("darksecai_models", exist_ok=True)
joblib.dump({"vectorizer": tfidf, "clf": xgb, "label_encoder": le}, "darksecai_models/severity_text_model.joblib")
print("Saved -> darksecai_models/severity_text_model.joblib with labels:", list(le.classes_))
