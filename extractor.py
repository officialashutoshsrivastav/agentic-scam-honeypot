import re

def extract_intelligence(text, store):
    store["upiIds"] += re.findall(r"\b\w+@\w+\b", text)
    store["phoneNumbers"] += re.findall(r"\+91\d{10}", text)
    store["phishingLinks"] += re.findall(r"https?://\S+", text)

    keywords = ["urgent", "verify", "blocked", "suspend"]
    store["suspiciousKeywords"] += [k for k in keywords if k in text.lower()]