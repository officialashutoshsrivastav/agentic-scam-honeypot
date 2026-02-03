conversation_store = {}

def get_history(session_id):
    return conversation_store.get(session_id, [])

def update_history(session_id, sender, text, timestamp):
    conversation_store.setdefault(session_id, []).append({
        "sender": sender,
        "text": text,
        "timestamp": timestamp
    })