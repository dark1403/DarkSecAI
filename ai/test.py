from predict_unified import predict_severity, suggest_cwe

finding_text = (
  "Missing Content-Security-Policy; inline <script> on login page; "
  "X-Powered-By header reveals framework; mixed active content detected"
)

conf, sev = predict_severity(finding_text)
cwe = suggest_cwe(finding_text, k=3)

print("Predicted severity:", sev, "confidence:", round(conf, 3))
for r in cwe:
    print(r.get("CWE-ID"), "|", r.get("Name"))
    print("Mitigations:", r.get("Potential Mitigations"))