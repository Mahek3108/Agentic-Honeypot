print("MAIN.PY IS RUNNING")

import json
import time
from fastapi import FastAPI, Request, Depends
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

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

# ✅ REQUIRED FOR GUVI TESTER
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ REQUIRED: OPTIONS HANDLER
@app.options("/{path:path}")
async def options_handler(path: str):
    return {"status": "ok"}


@app.post("/honeypot")
async def honeypot_endpoint(
    request: Request,
    _=Depends(verify_api_key)
):
    try:
        payload = await request.json()
    except Exception as e:
        raw = await request.body()
        try:
            raw_text = raw.decode("utf-8", errors="replace")
        except Exception:
            raw_text = str(raw)
        print(f"Failed to parse JSON: {e}; raw body: {raw_text}")
        return {
            "status": "success",
            "reply": "Could not parse request"
        }

    try:
        message = payload.get("message", {})
        message_text = str(message.get("text", "")).strip()
        
        if not message_text:
            return {
                "status": "success",
                "reply": "Hello?"
            }
        
        session_id = str(payload.get("sessionId", "unknown")).strip()
        history = payload.get("conversationHistory", [])
    except Exception as e:
        return {
            "status": "success",
            "reply": "Error reading message"
        }

    try:
        session = get_session(session_id)

        # increment message counter
        session["messages_exchanged"] = session.get("messages_exchanged", 0) + 1

        if not session.get("scam_detected"):
            session["scam_detected"] = detect_scam(message_text)

        intel = extract_intelligence(message_text)
        for k in intel:
            if k in session["extracted"]:
                session["extracted"][k].update(intel[k])

        if session.get("scam_detected"):
            reply = generate_agent_reply(message_text, history, session["extracted"])
        else:
            reply = generate_casual_reply(message_text)

        reply = str(reply).strip()

        # update process status
        if session.get("scam_detected") and session.get("process_status") != "in_progress":
            session["process_status"] = "in_progress"

        agent_notes = ""
        if session.get("scam_detected"):
            try:
                agent_notes = generate_agent_notes_llm(
                    extracted=session["extracted"],
                    last_message=message_text,
                )
            except Exception:
                agent_notes = ""

        # decide whether to send final callback
        should_callback = (
            session.get("scam_detected")
            and not session.get("callback_sent", False)
            and (
                bool(session["extracted"]["bank_accounts"]) or bool(session["extracted"]["upi_ids"]) or len(history) + 1 >= 6
            )
        )

        if should_callback:
            payload = {
                "sessionId": session_id,
                "scamDetected": True,
                "totalMessagesExchanged": len(history) + 1,
                "extractedIntelligence": {
                    "bankAccounts": list(session["extracted"].get("bank_accounts", [])),
                    "upiIds": list(session["extracted"].get("upi_ids", [])),
                    "phishingLinks": list(session["extracted"].get("phishing_urls", [])),
                    "phoneNumbers": list(session["extracted"].get("phone_numbers", [])),
                    "suspiciousKeywords": list(session["extracted"].get("suspicious_keywords", [])),
                },
                "agentNotes": agent_notes,
            }

            # debug log the callback payload
            print("GUVI CALLBACK PAYLOAD:", json.dumps(payload, ensure_ascii=False))

            try:
                send_final_callback(
                    session_id=session_id,
                    scam_detected=True,
                    total_messages=len(history) + 1,
                    extracted=session["extracted"],
                    agent_notes=agent_notes,
                )
                session["callback_sent"] = True
                session["process_status"] = "completed"
            except Exception as cb_e:
                print(f"Callback error: {cb_e}")

        # build conversation history to return
        incoming_entry = {"sender": message.get("sender", "scammer"), "text": message_text, "timestamp": int(time.time() * 1000)}
        agent_entry = {"sender": "agent", "text": reply, "timestamp": int(time.time() * 1000)}

        convo = [incoming_entry, agent_entry]

        return {
            "status": "success",
            "data": {
                "processStatus": session.get("process_status", "started"),
                "conversationHistory": convo,
            },
        }

    except Exception as e:
        print(f"Endpoint error: {e}")
        return {"status": "success", "data": {"processStatus": "started", "conversationHistory": []}}


@app.get("/")
def health():
    return {"status": "alive"}