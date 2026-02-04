from fastapi import Header, HTTPException

# def verify_api_key(x_api_key: str = Header(None)):
#     # GUVI sometimes doesn't send API key
#     if x_api_key is None:
#         return
#     if x_api_key != "changeme":
#         raise HTTPException(status_code=403, detail="Invalid API key")
# from fastapi import Header, HTTPException

async def verify_api_key(x_api_key: str = Header(None)):
   
    print(f"DEBUG: Header Key received is: {x_api_key}")
    return x_api_key