SCAM_KEYWORDS = [
    "account blocked", "verify", "urgent",
    "upi", "send money", "bank", "suspend"
]

def is_scam(text: str) -> bool:
    score = sum(1 for kw in SCAM_KEYWORDS if kw in text.lower())
    return score >= 2