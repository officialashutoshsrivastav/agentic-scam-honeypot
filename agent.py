import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a normal Indian user.
You are worried but polite.
Do not accuse or mention scam.
Ask natural follow-up questions.
Try to understand the issue.
"""

# def generate_reply(history):
#     try:
#         messages = [{"role": "system", "content": SYSTEM_PROMPT}]
#         for h in history:
#             role = "assistant" if h["sender"] == "user" else "user"
#             messages.append({"role": role, "content": h["text"]})

#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=messages,
#             temperature=0.7
#         )

#         return response.choices[0].message.content

#     except Exception as e:
#         print("LLM ERROR:", e)
#         return "I am a bit confused. Can you explain again?"
def generate_reply(history):
    last_msg = history[-1]["text"].lower()

    # ===== BANK ACCOUNT THREAT =====
    if "account" in last_msg and "blocked" in last_msg:
        return "Which bank is this about? I haven't received any official message."

    # ===== UPI FRAUD =====
    if "upi" in last_msg:
        return "Why do you need my UPI ID? I thought banks never ask for that."

    # ===== URGENCY / VERIFY =====
    if "verify" in last_msg or "urgent" in last_msg:
        return "I am at work right now. What will happen if I don't verify immediately?"

    # ===== OTP / PIN =====
    if "otp" in last_msg or "pin" in last_msg:
        return "I cannot share OTP or PIN. Is there any other way?"

    # ===== LINK / PHISHING =====
    if "http" in last_msg or "www" in last_msg:
        return "I am not able to open links. Can you explain what this is about?"

    # ===== PAYMENT / TRANSFER =====
    if "send money" in last_msg or "transfer" in last_msg:
        return "Why do I need to send money for verification?"

    # ===== DEFAULT HUMAN FALLBACK =====
    return "I don't fully understand this. Can you please explain again?"
