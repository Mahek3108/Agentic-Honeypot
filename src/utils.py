from fastapi import Header, HTTPException

def verify_api_key(x_api_key: str = Header(None)):
 
    if x_api_key != "changeme":
        raise HTTPException(status_code=403, detail="Invalid API key")
from fastapi import Header, HTTPException
