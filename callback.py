import requests

def send_callback(session_id, total, intelligence):
    payload = {
        "sessionId": session_id,
        "scamDetected": True,
        "totalMessagesExchanged": total,
        "extractedIntelligence": intelligence,
        "agentNotes": "Used urgency and payment redirection"
    }

    requests.post(
        "https://hackathon.guvi.in/api/updateHoneyPotFinalResult",
        json=payload,
        timeout=5
    )