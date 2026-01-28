
print("🔥 MAIN.PY IS RUNNING 🔥")
import time
from fastapi import FastAPI, Depends
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


app = FastAPI(title=APP_NAME)


@app.post("/honeypot", response_model=HoneypotResponse)
def honeypot_endpoint(
    payload: HoneypotRequest,
    _=Depends(verify_api_key)
):
    session = get_session(payload.sessionId)
    # ---- Strategy State Transition ----
    if session["scam_detected"]:
        if session["strategy_state"] == "HOOK":
            # After first reply → stall
            if len(payload.conversationHistory) >= 1:
                session["strategy_state"] = "STALL"
    elif session["strategy_state"] == "STALL":
        # If no intel yet and enough turns → pivot
        if (
            len(payload.conversationHistory) >= 2
            and not session["extracted"]["upi_ids"]
        ):
            session["strategy_state"] = "PIVOT"

    # Step 1: Scam detection
    if not session["scam_detected"]:
        session["scam_detected"] = detect_scam(payload.latestMessage.text)

    # Step 2: Intelligence extraction
    intel = extract_intelligence(payload.latestMessage.text)

    for key in intel:
        session["extracted"][key].update(intel[key])

    # Step 3: Agent reply
    turns = len(payload.conversationHistory)
    latest_text = payload.latestMessage.text.lower()

# --- Surprise reaction for first alarming message ---
    if (
        session["scam_detected"]
        and len(payload.conversationHistory) == 0
        and any(
            kw in latest_text
            for kw in ["hacked", "blocked", "compromised", "suspended"]
        )
    ):
        agent_reply = "What? Aap kaun bol rahe ho? Which account are you talking about?"
    else:
        agent_reply = (
            generate_agent_reply(
                f"[STRATEGY:{session['strategy_state']}] {payload.latestMessage.text}",
                payload.conversationHistory,
                session["extracted"]
            )
            if session["scam_detected"]
            else "Okay."
        )

    duration = int(time.time() - session["start_time"])
    return HoneypotResponse(
        scam_detected=session["scam_detected"],
    agent_active=session["scam_detected"],
    engagement=EngagementMetrics(
        turns=turns,
        duration_seconds=duration
    ),
    extracted_intelligence=ExtractedIntelligence(
        upi_ids=list(session["extracted"]["upi_ids"]),
        bank_accounts=list(session["extracted"]["bank_accounts"]),
        phishing_urls=list(session["extracted"]["phishing_urls"])
    ),
    agent_reply=agent_reply
)