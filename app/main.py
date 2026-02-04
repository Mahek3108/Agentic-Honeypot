print("MAIN.PY IS RUNNING")

import time
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse

from app.utils import verify_api_key
from app.config import APP_NAME
from app.gatekeeper import detect_scam
from app.memory import get_session
from app.extractor import extract_intelligence
from app.persona_agent import generate_agent_reply
from app.casual_llm import generate_casual_reply
from app.callback import send_final_callback
from app.agent_notes_llm import generate_agent_notes_llm

app = FastAPI(title=APP_NAME)


@app.post("/honeypot")
async def honeypot_endpoint(
    request: Request,
    _=Depends(verify_api_key)
):
    """
    GUVI Honeypot endpoint - returns ONLY status and reply.
    """
    
    # Parse incoming request
    try:
        payload = await request.json()
    except Exception:
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "reply": "Sorry, could not understand the message"
            }
        )
    
    # Extract fields safely
    try:
        message_obj = payload.get("message", {})
        message_text = message_obj.get("text", "").strip()
        history = payload.get("conversationHistory", [])
        session_id = payload.get("sessionId", "unknown")
        
        if not message_text:
            return JSONResponse(
                status_code=200,
                content={
                    "status": "success",
                    "reply": "Hello, kaun bol raha hai?"
                }
            )
    except Exception:
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "reply": "Kya hua? Samajh nahi aaya"
            }
        )
    
    # Get session
    session = get_session(session_id)
    
    # Scam detection
    if not session["scam_detected"]:
        try:
            session["scam_detected"] = detect_scam(message_text)
        except Exception:
            session["scam_detected"] = False
    
    # Intelligence extraction
    try:
        intel = extract_intelligence(message_text)
        for k in intel:
            if k in session["extracted"]:
                session["extracted"][k].update(intel[k])
    except Exception:
        pass
    
    # Generate reply
    turns = len(history)
    
    try:
        if session["scam_detected"]:
            agent_reply = generate_agent_reply(
                message_text,
                history,
                session["extracted"]
            )
        else:
            agent_reply = generate_casual_reply(message_text)
    except Exception:
        agent_reply = "Thoda samajh nahi aaya, phir se batao"
    
    # Generate agent notes (for callback, not response)
    agent_notes = ""
    if session["scam_detected"]:
        try:
            agent_notes = generate_agent_notes_llm(
                extracted=session["extracted"],
                last_message=message_text
            )
        except Exception:
            agent_notes = "Scammer used social engineering tactics"
    
    # Send GUVI callback (once per session)
    if (
        session["scam_detected"]
        and not session.get("callback_sent", False)
        and (
            session["extracted"]["bank_accounts"]
            or session["extracted"]["upi_ids"]
            or turns >= 6
        )
    ):
        try:
            send_final_callback(
                session_id=session_id,
                scam_detected=True,
                total_messages=turns + 1,
                extracted=session["extracted"],
                agent_notes=agent_notes
            )
            session["callback_sent"] = True
        except Exception as e:
            print(f"Callback failed: {e}")
    
    # Return ONLY status and reply (GUVI requirement)
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "reply": agent_reply
        }
    )


@app.get("/")
def health():
    return {"status": "alive"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": APP_NAME}