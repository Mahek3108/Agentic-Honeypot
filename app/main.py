print("MAIN.PY IS RUNNING")

import time
import json
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse

from app.schemas import (
    HoneypotRequest,
    HoneypotResponse,
    EngagementMetrics,
    ExtractedIntelligence
)
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
        # Parse raw JSON to bypass pydantic validation
        payload = await request.json()
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "reply": "Invalid JSON"}
        )

    try:
        # Extract message and history with safe defaults
        message_obj = payload.get("message", {})
        message_text = message_obj.get("text", "")
        history = payload.get("conversationHistory", [])
        session_id = payload.get("sessionId", "unknown")
        
        if not message_text:
            return {"status": "success", "reply": "Unable to process empty message"}
    except Exception as e:
        return {"status": "success", "reply": "Unable to process message"}

    # Session
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
    # -----------------------------
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
    # Agent notes
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
            or turns >= 6
        )
    ):
        send_final_callback(
            session_id=session_id,
            scam_detected=True,
            total_messages=turns + 1,
            extracted=session["extracted"],
            agent_notes=agent_notes
        )
        session["callback_sent"] = True

    # -----------------------------
    # Response
    duration = int(time.time() - session["start_time"])

    # Return minimal GUVI-compliant response
    return {
        "status": "success",
        "reply": agent_reply
    }


@app.get("/")
def health():
    return {"status": "alive"}
