print("MAIN.PY IS RUNNING")

import json
import time
from fastapi import FastAPI, Request, Depends
from fastapi.responses import Response, JSONResponse
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
    return JSONResponse(content={"status": "ok"})


@app.post("/honeypot")
async def honeypot_endpoint(
    request: Request,
    _=Depends(verify_api_key)
):
    try:
        payload = await request.json()
    except Exception:
        return JSONResponse({"status": "success", "reply": "Hello?"})

    message = payload.get("message")
    if not message or "text" not in message:
        return JSONResponse({"status": "success", "reply": "Hello?"})

    message_text = str(message["text"]).replace("\n", " ").strip()
    session_id = payload.get("sessionId", "unknown")
    history = payload.get("conversationHistory", [])

    session = get_session(session_id)

    if not session["scam_detected"]:
        session["scam_detected"] = detect_scam(message_text)

    intel = extract_intelligence(message_text)
    for k in intel:
        session["extracted"][k].update(intel[k])

    if session["scam_detected"]:
        reply = generate_agent_reply(message_text, history, session["extracted"])
    else:
        reply = generate_casual_reply(message_text)

    reply = reply.replace("\n", " ").strip()

    agent_notes = ""
    if session["scam_detected"]:
        agent_notes = generate_agent_notes_llm(
            extracted=session["extracted"],
            last_message=message_text
        )

    if (
        session["scam_detected"]
        and not session.get("callback_sent")
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

    return JSONResponse(
        content={
            "status": "success",
            "reply": reply
        }
    )


@app.get("/")
def health():
    return {"status": "alive"}