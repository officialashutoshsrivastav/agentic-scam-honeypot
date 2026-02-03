from fastapi import FastAPI, Depends, Body
from auth import verify_api_key
from scam_detector import is_scam
from agent import generate_reply
from memory import get_history, update_history
from extractor import extract_intelligence
from callback import send_callback

app = FastAPI()

# In-memory intelligence store
intelligence_store = {}


@app.get("/api/scam-event")
def health_check():
    # For GUVI / uptime / reachability tests
    return {
        "status": "success",
        "message": "Honeypot endpoint is live"
    }


@app.post("/api/scam-event")
def scam_event(
    data: dict = Body(default=None),
    api_key=Depends(verify_api_key)
):
    # 🔹 Handle empty / invalid body (GUVI tester fix)
    if not data or "message" not in data or "sessionId" not in data:
        return {
            "status": "success",
            "reply": "Endpoint reachable and authenticated."
        }

    session_id = data["sessionId"]
    msg = data["message"]

    # Ensure required fields exist
    if "text" not in msg or "sender" not in msg or "timestamp" not in msg:
        return {
            "status": "success",
            "reply": "Invalid message format handled."
        }

    # Conversation memory
    history = get_history(session_id)
    update_history(session_id, msg["sender"], msg["text"], msg["timestamp"])

    # Non-scam flow
    if not is_scam(msg["text"]):
        return {
            "status": "success",
            "reply": "Okay, thanks for informing."
        }

    # Initialize intelligence store per session
    intelligence_store.setdefault(session_id, {
        "bankAccounts": [],
        "upiIds": [],
        "phishingLinks": [],
        "phoneNumbers": [],
        "suspiciousKeywords": []
    })

    # Extract intelligence
    extract_intelligence(msg["text"], intelligence_store[session_id])

    # Generate agent reply
    reply = generate_reply(history + [msg])
    update_history(session_id, "user", reply, msg["timestamp"])

    # Final callback after sufficient engagement
    if len(get_history(session_id)) >= 8:
        send_callback(
            session_id=session_id,
            total_messages=len(get_history(session_id)),
            intelligence=intelligence_store[session_id]
        )

    return {
        "status": "success",
        "reply": reply
    }
