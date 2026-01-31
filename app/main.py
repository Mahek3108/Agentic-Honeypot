print("MAIN.PY IS RUNNING")

import time
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
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

# ========================================
# CORS Middleware - CRITICAL FOR GUVI
# ========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],              # Allow all origins (GUVI needs this)
    allow_credentials=True,           # Changed to True
    allow_methods=["*"],              # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],              # Allow all headers
    expose_headers=["*"],             # Expose all headers
)

# ========================================
# Global OPTIONS handler for all paths
# ========================================
@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    """Handle CORS preflight for all paths"""
    return JSONResponse(
        content={"status": "ok"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )

# ========================================
# Main Honeypot Endpoint
# ========================================
@app.post("/honeypot", response_model=HoneypotResponse)
async def honeypot_endpoint(
    request: Request,
    payload: HoneypotRequest,
    _=Depends(verify_api_key)
):
    # -----------------------------
    # Session
    # -----------------------------
    session = get_session(payload.sessionId)

    # -----------------------------
    # Normalize incoming message (GUVI compatible)
    # -----------------------------
    incoming = payload.message or payload.latestMessage
    if not incoming:
        return HoneypotResponse(
            status="error",
            reply="No message provided",
            agent_reply="No message provided",
            scam_detected=False,
            agent_active=False,
            engagement=EngagementMetrics(turns=0, duration_seconds=0),
            extracted_intelligence=ExtractedIntelligence(),
            agent_notes=""
        )

    message_text = incoming.text

    # -----------------------------
    # Strategy State Transition
    # -----------------------------
    if session["scam_detected"]:
        if session["strategy_state"] == "HOOK":
            if len(payload.conversationHistory) >= 1:
                session["strategy_state"] = "STALL"

        elif session["strategy_state"] == "STALL":
            if (
                len(payload.conversationHistory) >= 2
                and not session["extracted"]["upi_ids"]
            ):
                session["strategy_state"] = "PIVOT"

    # -----------------------------
    # Step 1: Scam Detection
    # -----------------------------
    if not session["scam_detected"]:
        session["scam_detected"] = detect_scam(message_text)

    # -----------------------------
    # Step 2: Intelligence Extraction
    # -----------------------------
    intel = extract_intelligence(message_text)
    for key in intel:
        session["extracted"][key].update(intel[key])

    # -----------------------------
    # Step 3: Agent Reply
    # -----------------------------
    turns = len(payload.conversationHistory)

    if session["scam_detected"]:
        agent_reply = generate_agent_reply(
            f"[STRATEGY:{session['strategy_state']}] {message_text}",
            payload.conversationHistory,
            session["extracted"]
        )
    else:
        agent_reply = generate_casual_reply(message_text)
    
    agent_notes = ""
    if session["scam_detected"]:
        agent_notes = generate_agent_notes_llm(
            extracted=session["extracted"],
            last_message=message_text
        )

    # -----------------------------
    # Step 4: FINAL GUVI CALLBACK
    # -----------------------------
    if (
        session["scam_detected"]
        and not session.get("callback_sent", False)
        and (
            session["extracted"]["bank_accounts"]
            or session["extracted"]["phishing_urls"]
            or len(payload.conversationHistory) >= 8
        )
    ):
        send_final_callback(
            session_id=payload.sessionId,
            scam_detected=True,
            total_messages=len(payload.conversationHistory) + 1,
            extracted=session["extracted"],
            agent_notes=agent_notes
        )
        session["callback_sent"] = True

    # -----------------------------
    # Step 5: Response (GUVI + Extended)
    # -----------------------------
    duration = int(time.time() - session["start_time"])

    return HoneypotResponse(
        status="success",
        
        # GUVI-required
        reply=agent_reply,
        
        # internal / extended
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
            emails=list(session["extracted"].get("emails", [])),
            suspicious_keywords=list(session["extracted"]["suspicious_keywords"]),
            misc=session["extracted"].get("misc", {})
        ),
        
        agent_notes=agent_notes
    )

# ========================================
# Health Check
# ========================================
@app.get("/")
async def health():
    return {"status": "alive", "service": APP_NAME}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": APP_NAME}