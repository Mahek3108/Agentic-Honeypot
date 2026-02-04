print("MAIN.PY IS RUNNING")

import time
from fastapi import FastAPI, Depends, Request
from fastapi.responses import Response
import json
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
    try:
        payload = await request.json()
    except Exception:
        return {
            "status": "success",
            "reply": "Could not understand"
        }

    try:
        message_obj = payload.get("message", {})
        message_text = message_obj.get("text", "").strip()
        
        if not message_text:
            return {
                "status": "success",
                "reply": "Hello?"
            }
        
        session_id = payload.get("sessionId", "unknown")
        history = payload.get("conversationHistory", [])
    except Exception:
        return {
            "status": "success",
            "reply": "Error reading message"
        }

    session = get_session(session_id)

    # -----------------------------
    # Scam detection
    # -----------------------------
    if not session["scam_detected"]:
        session["scam_detected"] = detect_scam(message_text)

    # -----------------------------
    # Intelligence extraction
    # -----------------------------
    intel = extract_intelligence(message_text)
    for k in intel:
        session["extracted"][k].update(intel[k])

    # -----------------------------
    # Agent reply
    history = history or []
    turns = len(history)

    if session["scam_detected"]:
        agent_reply = generate_agent_reply(
            message_text,
            history,
            session["extracted"]
        )
    else:
        agent_reply = generate_casual_reply(message_text)

    # -----------------------------
    # Agent notes (LLM)
    # -----------------------------
    agent_notes = ""
    if session["scam_detected"]:
        agent_notes = generate_agent_notes_llm(
            extracted=session["extracted"],
            last_message=message_text
        )

    # -----------------------------
    # FINAL GUVI CALLBACK (ONCE)
    # -----------------------------
    if (
        session["scam_detected"]
        and not session.get("callback_sent", False)
        and (
            session["extracted"]["bank_accounts"]
            or session["extracted"]["upi_ids"]
            or len(history) >= 6
        )
    ):
        send_final_callback(
            session_id=payload.sessionId,
            scam_detected=True,
            total_messasession_i
            extracted=session["extracted"],
            agent_notes=agent_notes
        )
        session["callback_sent"] = True

    duration = int(time.time() - session["start_time"])

    # Return ONLY status and reply (GUVI requirement)
    return Response(
        content=json.dumps({
            "status": "success",
            "reply": str(agent_reply).strip()
        }),
        status_code=200,
        media_type="application/json"
    )

@app.get("/")
def health():
    return {"status": "alive"}