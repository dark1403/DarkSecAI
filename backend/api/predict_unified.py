
# predict_unified.py
# Given a finding text (e.g., features converted to natural language), returns severity + top CWE suggestions.
import joblib, numpy as np

def prob_to_severity_from_probs(probs, classes):
    # pick top class and return label
    idx = int(np.argmax(probs))
    return classes[idx]

sev = joblib.load("./darksecai_models/severity_text_model.joblib")
tfidf, clf, le = sev["vectorizer"], sev["clf"], sev["label_encoder"]

cwe = joblib.load("./darksecai_models/cwe_retriever.joblib")
vec2, nn, texts, meta = cwe["vectorizer"], cwe["nn"], cwe["texts"], cwe["meta"]

def predict_severity(finding_text: str):
    X = tfidf.transform([finding_text])
    probs = clf.predict_proba(X)[0]
    label = prob_to_severity_from_probs(probs, le.classes_)
    return float(np.max(probs)), label

def suggest_cwe(finding_text: str, k: int = 5):
    Y = vec2.transform([finding_text])
    dist, idx = nn.kneighbors(Y, n_neighbors=k, return_distance=True)
    out = []
    for d, i in zip(dist[0], idx[0]):
        row = meta.iloc[i].to_dict()
        row["similarity"] = float(1.0 - d)
        out.append(row)
    return out

if __name__ == "__main__":
    demo = "Missing Content-Security-Policy header allows inline JavaScript and external scripts on login page"
    p, sev = predict_severity(demo)
    print("Severity:", sev, " confidence:", round(p,4))
    print("Top CWE:")
    for r in suggest_cwe(demo, k=3):
        print("-", r.get("CWE-ID"), "|", r.get("Name"), "| sim:", round(r["similarity"],3))
