from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional, Dict, Any, Union


class IncomingMessage(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra='allow')
    
    sender: Optional[str] = None
    text: str
    timestamp: Optional[Union[int, str, float]] = None


class HoneypotRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra='allow')
    
    sessionId: strprint("MAIN.PY IS RUNNING")

import time
import json
from fastapi import FastAPI, Request, Depends
from fastapi.responses import Response

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
    # -----------------------------
    # Parse raw JSON (GUVI safe)
    # -----------------------------
    try:
        payload = await request.json()
    except Exception:
        return Response(
            content=json.dumps({"status": "success", "reply": "Hello?"}),
            media_type="application/json"
        )

    message = payload.get("message")
    if not message or "text" not in message:
        return Response(
            content=json.dumps({"status": "success", "reply": "Hello?"}),
            media_type="application/json"
        )

    message_text = str(message.get("text")).strip()
    session_id = payload.get("sessionId", "unknown")
    history = payload.get("conversationHistory", [])

    # -----------------------------
    # Session
    # -----------------------------
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
    if session["scam_detected"]:
        reply = generate_agent_reply(
            message_text,
            history,
            session["extracted"]
        )
    else:
        reply = generate_casual_reply(message_text)

    reply = reply.replace("\n", " ").strip() # IMPORTANT

    # -----------------------------
    # Agent notes (for callback)
    # -----------------------------
    agent_notes = ""
    if session["scam_detected"]:
        agent_notes = generate_agent_notes_llm(
            extracted=session["extracted"],
            last_message=message_text
        )

    # -----------------------------
    # FINAL CALLBACK (ONCE)
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
            session_id=session_id,
            scam_detected=True,
            total_messages=len(history) + 1,
            extracted=session["extracted"],
            agent_notes=agent_notes
        )
        session["callback_sent"] = True

    # -----------------------------
    # GUVI RESPONSE (STRICT)
    # -----------------------------
    return Response(
        content=json.dumps({
            "status": "success",
            "reply": reply
        }),
        status_code=200,
        media_type="application/json"
    )


@app.get("/")
def health():
    return {"status": "alive"}
    message: IncomingMessage
    conversationHistory: List[Dict[str, Any]] = []
    metadata: Optional[Dict[str, Any]] = None


class EngagementMetrics(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    turns: int
    duration_seconds: Optional[int] = Field(None, alias="durationSeconds")


class ExtractedIntelligence(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    upi_ids: List[str] = Field(default_factory=list, alias="upiIds")
    bank_accounts: List[str] = Field(default_factory=list, alias="bankAccounts")
    phishing_urls: List[str] = Field(default_factory=list, alias="phishingLinks")
    phone_numbers: List[str] = Field(default_factory=list, alias="phoneNumbers")
    suspicious_keywords: List[str] = Field(default_factory=list, alias="suspiciousKeywords")


class HoneypotResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    status: str
    reply: str

    scam_detected: bool = Field(..., alias="scamDetected")
    agent_active: bool = Field(..., alias="agentActive")

    engagement: EngagementMetrics
    extracted_intelligence: ExtractedIntelligence = Field(..., alias="extractedIntelligence")

    agent_reply: str = Field(..., alias="agentReply")
    agent_notes: str = Field(..., alias="agentNotes")

