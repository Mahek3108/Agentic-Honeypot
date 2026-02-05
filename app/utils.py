# from fastapi import Header, HTTPException

# # def verify_api_key(x_api_key: str = Header(None)):
# #     # GUVI sometimes doesn't send API key
# #     if x_api_key is None:
# #         return
# #     if x_api_key != "changeme":
# #         raise HTTPException(status_code=403, detail="Invalid API key")
# # from fastapi import Header, HTTPException

# async def verify_api_key(x_api_key: str = Header(None)):
   
#     print(f"DEBUG: Header Key received is: {x_api_key}")
#     return x_api_key

from fastapi import Header, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN

API_KEY = "tera_secret_key_yahan_likho" # Jo GUVI mein bharna hai
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

async def verify_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        # Ye line bypass rokti hai
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )