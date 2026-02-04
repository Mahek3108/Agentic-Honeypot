print("MAIN.PY IS RUNNING")

import time
import json
from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

from app.config import APP_NAME
from app.gatekeeper import detect_scam
from app.memory import get_session
from app.extractor import extract_intelligence
from app.persona_agent import generate_agent_reply
from app.casual_llm import generate_casual_reply
from app.callback import send_final_callback
from app.agent_notes_llm import generate_agent_notes_llm

app = FastAPI(title=APP_NAME)

# Add CORS middleware for GUVI tester
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/honeypot")
async def honeypot_endpoint(request: Request):
    """
    GUVI Honeypot Endpoint
    Returns ONLY: {"status": "success", "reply": "..."}
    """
    
    # Parse incoming request
    try:
        payload = await request.json()
        message_text = payload.get("message", {}).get("text", "").strip()
        history = payload.get("conversationHistory", [])
        session_id = payload.get("sessionId", "unknown")
        
        if not message_text:
            return Response(
                content=json.dumps(
                    {"status": "success", "reply": "Hello, kaun bol raha hai?"},
                    ensure_ascii=False,
                    separators=(',', ':')
                ),
                media_type="application/json",
                status_code=200
            )
            
    except Exception as e:
        print(f"❌ Parse error: {e}")
        return Response(
            content=json.dumps(
                {"status": "success", "reply": "Sorry, I didn't understand"},
                ensure_ascii=False,
                separators=(',', ':')
            ),
            media_type="application/json",
            status_code=200
        )
    
    # Get or create session
    session = get_session(session_id)
    
    # Scam detection with error handling
    if not session["scam_detected"]:
        try:
            session["scam_detected"] = detect_scam(message_text)
        except Exception as e:
            print(f"❌ Detection error: {e}")
            session["scam_detected"] = False
    
    # Extract intelligence with error handling
    try:
        intel = extract_intelligence(message_text)
        for k in intel:
            if k in session["extracted"]:
                session["extracted"][k].update(intel[k])
    except Exception as e:
        print(f"❌ Extraction error: {e}")
    
    # Generate reply with fallback
    turns = len(history)
    agent_reply = "I don't understand"
    
    try:
        if session["scam_detected"]:
            agent_reply = generate_agent_reply(
                message_text,
                history,
                session["extracted"]
            )
        else:
            agent_reply = generate_casual_reply(message_text)
            
    except Exception as e:
        print(f"❌ Reply generation error: {e}")
        # Intelligent fallback based on context
        if session["scam_detected"]:
            if "block" in message_text.lower() or "suspend" in message_text.lower():
                agent_reply = "Why is my account blocked? Who are you?"
            elif "upi" in message_text.lower() or "payment" in message_text.lower():
                agent_reply = "I don't know how to do UPI. Can you help?"
            elif "link" in message_text.lower() or "http" in message_text.lower():
                agent_reply = "The link is not opening. What should I do?"
            else:
                agent_reply = "I'm confused. Please explain properly"
        else:
            agent_reply = "Hello, kaun bol raha hai?"
    
    # Generate agent notes for callback (not in response)
    agent_notes = ""
    if session["scam_detected"]:
        try:
            agent_notes = generate_agent_notes_llm(
                extracted=session["extracted"],
                last_message=message_text
            )
        except Exception as e:
            print(f"❌ Agent notes error: {e}")
            agent_notes = "Scammer used social engineering tactics"
    
    # Send final callback to GUVI (once per session)
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
            print(f"✅ Callback sent for session: {session_id}")
        except Exception as e:
            print(f"❌ Callback error: {e}")
    
    # Return ONLY status and reply (GUVI requirement)
    return {
        "status": "success",
        "reply": str(agent_reply).strip()
    }


@app.get("/")
def health():
    """Health check endpoint"""
    return {"status": "alive"}


@app.get("/health")
def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": APP_NAME,
        "timestamp": int(time.time())
    }