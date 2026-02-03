from fastapi import FastAPI, Depends, Request
from auth import verify_api_key
from scam_detector import is_scam
from agent import generate_reply
from memory import get_history, update_history
from extractor import extract_intelligence
from callback import send_callback

app = FastAPI()
intelligence_store = {}


@app.get("/api/scam-event")
def health_check():
    return {"status": "success", "message": "Honeypot endpoint is live"}


@app.post("/api/scam-event")
async def scam_event(
    request: Request,
    api_key=Depends(verify_api_key)
):
    # 🔥 RAW BODY HANDLING (GUVI FIX)
    try:
        data = await request.json()
    except Exception:
        return {
            "status": "success",
            "reply": "Endpoint reachable and authenticated."
        }

    if not isinstance(data, dict) or "message" not in data or "sessionId" not in data:
        return {
            "status": "success",
            "reply": "Endpoint reachable and authenticated."
        }

    session_id = data["sessionId"]
    msg = data["message"]

    if not all(k in msg for k in ("text", "sender", "timestamp")):
        return {
            "status": "success",
            "reply": "Invalid message format handled."
        }

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
        send_callback(
            session_id=session_id,
            total_messages=len(get_history(session_id)),
            intelligence=intelligence_store[session_id]
        )

    return {"status": "success", "reply": reply}
