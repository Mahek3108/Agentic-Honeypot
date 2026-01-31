# from fastapi import Header, HTTPException
# from typing import Optional
# from app.config import API_KEY


# def verify_api_key(x_api_key: Optional[str] = Header(None)):
#     """
#     Verify API key from header.
#     Allow requests without API key if API_KEY is not set (for testing).
#     """
#     # If no API_KEY is configured, allow all requests
#     if API_KEY == "changeme" or not API_KEY:
#         return
    
#     # If API_KEY is configured, verify it
#     if x_api_key is None:
#         raise HTTPException(status_code=403, detail="Missing API key")
    
#     if x_api_key != API_KEY:
#         raise HTTPException(status_code=403, detail="Invalid API key")
from fastapi import Header, HTTPException
from app.config import API_KEY

def verify_api_key(x_api_key: str = Header(None)):
    # Allow GUVI tester + OPTIONS
    if x_api_key is None:
        return

    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
