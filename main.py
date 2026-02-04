#Agentic_Scam_HoneyPot
from fastapi import FastAPI, Depends
from auth import verify_api_key
from scam_detector import is_scam
from agent import generate_reply
from memory import get_history, update_history
from extractor import extract_intelligence
from callback import send_callback

app = FastAPI()
intelligence_store = {}

@app.post("/api/scam-event")
def scam_event(data: dict, api_key=Depends(verify_api_key)):
    session_id = data["sessionId"]
    msg = data["message"]

    history = get_history(session_id)
    update_history(session_id, msg["sender"], msg["text"], msg["timestamp"])

    if not is_scam(msg["text"]):
        return {"status": "success", "reply": "Okay, thanks for informing."}

    intelligence_store.setdefault(session_id, {
        "bankAccounts": [],
        "upiIds": [],
        "phishingLinks": [],
        "phoneNumbers": [],
        "suspiciousKeywords": []
    })

    extract_intelligence(msg["text"], intelligence_store[session_id])
    reply = generate_reply(history + [msg])
    update_history(session_id, "user", reply, msg["timestamp"])

    if len(get_history(session_id)) >= 8:
        send_callback(session_id, len(get_history(session_id)), intelligence_store[session_id])

    return {"status": "success", "reply": reply}
