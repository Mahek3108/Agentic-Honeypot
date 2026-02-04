from fastapi import Header, HTTPException
from app.config import API_KEY

def verify_api_key(x_api_key: str = Header(None)):
    # GUVI sometimes does NOT send API key
    if x_api_key is None:
        return
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
