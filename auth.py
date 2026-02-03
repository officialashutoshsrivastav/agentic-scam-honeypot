import os
from fastapi import Header, HTTPException
from dotenv import load_dotenv

load_dotenv()  # 👈 THIS LINE IS THE FIX

SECRET_KEY = os.getenv("API_KEY")

def verify_api_key(x_api_key: str = Header(...)):
    if not SECRET_KEY:
        raise HTTPException(status_code=500, detail="API_KEY not set in environment")

    if x_api_key != SECRET_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
