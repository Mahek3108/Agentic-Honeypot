
# from fastapi import Header, HTTPException
# from app.config import API_KEY

# def verify_api_key(x_api_key: str = Header(None)):
#     # Allow GUVI tester + OPTIONS
#     if x_api_key is None:
#         return

#     if x_api_key != API_KEY:
#         raise HTTPException(status_code=403, detail="Invalid API key")




from fastapi import Header, HTTPException, Request
from app.config import API_KEY

async def verify_api_key(request: Request, x_api_key: str = Header(None)):
    """
    Verify API key but allow:
    - OPTIONS requests (CORS preflight)
    - Requests without API key (for GUVI testing)
    """
    # Always allow OPTIONS requests (CORS preflight)
    if request.method == "OPTIONS":
        return
    
    # If no API key provided, allow it (GUVI tester compatibility)
    if x_api_key is None:
        return
    
    # If API key IS provided, validate it
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")