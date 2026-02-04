print("MAIN.PY IS RUNNING")

import time
import json
from fastapi import FastAPI, Depends, Body

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
def honeypot_endpoint(
    payload: HoneypotRequest,
    _=Depends(verify_api_key)
):
    try:
        # Extract message and history
        message_text = payload.message.text
        history = payload.conversationHistory
    except Exception as e:
        # Graceful fallback if request is malformed
        return {
            "status": "success",
            "reply": "Unable to process message",
            "scamDetected": False,
            "agentActive": False,
            "engagement": {"turns": 0, "durationSeconds": 0},
            "extractedIntelligence": {"upiIds": [], "bankAccounts": [], "phishingLinks": [], "phoneNumbers": [], "suspiciousKeywords": []},
            "agentReply": "Unable to process message",
            "agentNotes": ""
        }

    # -----------------------------
    # Session
    # -----------------------------
    session = get_session(payload.sessionId)

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
            session_id=payload.sessionId,
            scam_detected=True,
            total_messages=turns + 1,
            extracted=session["extracted"],
            agent_notes=agent_notes
        )
        session["callback_sent"] = True

    # -----------------------------
    # Response
    # -----------------------------
    duration = int(time.time() - session["start_time"])

    resp = HoneypotResponse(
        status="success",
        reply=agent_reply,
        agent_reply=agent_reply,
        scam_detected=session["scam_detected"],
        agent_active=session["scam_detected"],
        engagement=EngagementMetrics(
            turns=turns,
            duration_seconds=duration
        ),
        extracted_intelligence=ExtractedIntelligence(
            upi_ids=list(session["extracted"]["upi_ids"]),
            bank_accounts=list(session["extracted"]["bank_accounts"]),
            phishing_urls=list(session["extracted"]["phishing_urls"]),
            phone_numbers=list(session["extracted"]["phone_numbers"]),
            suspicious_keywords=list(session["extracted"]["suspicious_keywords"]),
        ),
        agent_notes=agent_notes
    )

    # Return minimal GUVI-compliant response
    return {
        "status": "success",
        "reply": agent_reply
    }


@app.get("/")
def health():
    return {"status": "alive"}
