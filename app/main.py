
from fastapi import FastAPI, Depends
from app.schemas import HoneypotRequest
from app.utils import verify_api_key
from app.gatekeeper import detect_scam
from app.memory import get_session
from app.extractor import extract_intelligence
from app.persona_agent import generate_agent_reply
from app.casual_llm import generate_casual_reply
from app.callback import send_final_callback
from app.agent_notes_llm import generate_agent_notes_llm

app = FastAPI(title="Agentic HoneyPot")


@app.post("/honeypot")
async def honeypot_endpoint(
    payload: HoneypotRequest,
    _=Depends(verify_api_key)
):
    # 🔹 REQUIRED: message MUST exist
    incoming = payload.message
    message_text = incoming.text.strip()

    session = get_session(payload.sessionId)
    #session["messages_exchanged"] = session.get("messages_exchanged", 0) + 1
    history = payload.conversationHistory or []
    
    # Scam detection
    if not session["scam_detected"]:
        session["scam_detected"] = detect_scam(message_text)

    # Intelligence extraction
    intel = extract_intelligence(message_text)
    for k in intel:
        session["extracted"][k].update(intel[k])
    # any_intel_found = any([
    #     session["extracted"].get("bank_accounts"),
    #     session["extracted"].get("upi_ids"),
    #     session["extracted"].get("phishing_urls"),
    #     session["extracted"].get("phone_numbers")
    # ])
    # Agent reply
    if session["scam_detected"]:
        reply = generate_agent_reply(message_text, history, session["extracted"])
    else:
        reply = generate_casual_reply(message_text)

    # Agent notes
    agent_notes = ""
    if session["scam_detected"]:
        agent_notes = generate_agent_notes_llm(
            extracted=session["extracted"],
            last_message=message_text
        )
    
    if (
        session["scam_detected"]
        # and not session.get("callback_sent", False)
        and len(history) >= 8
        
    ):
        send_final_callback(
            session_id=payload.sessionId,
            scam_detected=True,
            total_messages= len(history)+2,
            extracted=session["extracted"],
            agent_notes=agent_notes,
        session_start_time= session["start_time"]
        )
        session["callback_sent"] = True

    return {
        "status": "success",
        "reply": reply.strip()
    }
