
# # # print("MAIN.PY IS RUNNING")
# # # import time
# # # from fastapi import FastAPI, Depends
# # # from app.schemas import (
# # #     HoneypotRequest,
# # #     HoneypotResponse,
# # #     EngagementMetrics,
# # #     ExtractedIntelligence
# # # )
# # # from app.utils import verify_api_key
# # # from app.config import APP_NAME
# # # from app.gatekeeper import detect_scam
# # # from app.memory import get_session
# # # from app.extractor import extract_intelligence
# # # from app.persona_agent import generate_agent_reply
# # # from app.callback import send_final_callback

# # # from app.casual_llm import generate_casual_reply

# # # app = FastAPI(title=APP_NAME)


# # # @app.post("/honeypot", response_model=HoneypotResponse)
# # # def honeypot_endpoint(
# # #     payload: HoneypotRequest,
# # #     _=Depends(verify_api_key)
# # # ):
# # #     session = get_session(payload.sessionId)
# # #     # ---- Strategy State Transition ----
# # #     if session["scam_detected"]:
# # #         if session["strategy_state"] == "HOOK":
# # #             # After first reply → stall
# # #             if len(payload.conversationHistory) >= 1:
# # #                 session["strategy_state"] = "STALL"
# # #     elif session["strategy_state"] == "STALL":
# # #         # If no intel yet and enough turns → pivot
# # #         if (
# # #             len(payload.conversationHistory) >= 2
# # #             and not session["extracted"]["upi_ids"]
# # #         ):
# # #             session["strategy_state"] = "PIVOT"

# # #     # Step 1: Scam detection
# # #     if not session["scam_detected"]:
# # #         session["scam_detected"] = detect_scam(payload.latestMessage.text)

# # #     # Step 2: Intelligence extraction
# # #     intel = extract_intelligence(payload.latestMessage.text)

# # #     for key in intel:
# # #         session["extracted"][key].update(intel[key])

# # #     # Step 3: Agent reply
# # #     turns = len(payload.conversationHistory)
# # #     agent_reply = (
# # #     generate_agent_reply(
# # #         f"[STRATEGY:{session['strategy_state']}] {payload.latestMessage.text}",
# # #         payload.conversationHistory,
# # #         session["extracted"]
# # #     )
# # #     if session["scam_detected"]
# # #     else generate_casual_reply(payload.latestMessage.text)
# # # )

# # #     duration = int(time.time() - session["start_time"])
# # #     return HoneypotResponse(
# # #         scam_detected=session["scam_detected"],
# # #     agent_active=session["scam_detected"],
# # #     engagement=EngagementMetrics(
# # #         turns=turns,
# # #         duration_seconds=duration
# # #     ),
# # #     extracted_intelligence=ExtractedIntelligence(
# # #         upi_ids=list(session["extracted"]["upi_ids"]),
# # #         bank_accounts=list(session["extracted"]["bank_accounts"]),
# # #         phishing_urls=list(session["extracted"]["phishing_urls"])
# # #     ),
# # #     agent_reply=agent_reply
# # # )
# # print("MAIN.PY IS RUNNING")

# # import time
# # from fastapi import FastAPI, Depends

# # from app.schemas import (
# #     HoneypotRequest,
# #     HoneypotResponse,
# #     EngagementMetrics,
# #     ExtractedIntelligence
# # )
# # from app.utils import verify_api_key
# # from app.config import APP_NAME
# # from app.gatekeeper import detect_scam
# # from app.memory import get_session
# # from app.extractor import extract_intelligence
# # from app.persona_agent import generate_agent_reply
# # from app.casual_llm import generate_casual_reply
# # from app.callback import send_final_callback


# # app = FastAPI(title=APP_NAME)


# # @app.post("/honeypot", response_model=HoneypotResponse)
# # def honeypot_endpoint(
# #     payload: HoneypotRequest,
# #     _=Depends(verify_api_key)
# # ):
# #     session = get_session(payload.sessionId)
# #     # --- Normalize incoming message (supports tester + swagger) ---
# #     incoming = payload.latestMessage or payload.message

# #     if not incoming:
# #         raise ValueError("No incoming message found")

# #     message_text = incoming.text
# #     sender_role = incoming.role or incoming.sender or "scammer"

# #     # -----------------------------
# #     # Strategy State Transition
# #     # -----------------------------
# #     if session["scam_detected"]:
# #         if session["strategy_state"] == "HOOK":
# #             if len(payload.conversationHistory) >= 1:
# #                 session["strategy_state"] = "STALL"

# #         elif session["strategy_state"] == "STALL":
# #             if (
# #                 len(payload.conversationHistory) >= 2
# #                 and not session["extracted"]["upi_ids"]
# #             ):
# #                 session["strategy_state"] = "PIVOT"

# #     # -----------------------------
# #     # Step 1: Scam Detection
# #     # -----------------------------
# #     if not session["scam_detected"]:
# #         session["scam_detected"] = detect_scam(payload.latestMessage.text)

# #     # -----------------------------
# #     # Step 2: Intelligence Extraction
# #     # -----------------------------
# #     intel = extract_intelligence(payload.latestMessage.text)

# #     for key in intel:
# #         session["extracted"][key].update(intel[key])

# #     # -----------------------------
# #     # Step 3: Agent Reply
# #     # -----------------------------
# #     turns = len(payload.conversationHistory)

# #     if session["scam_detected"]:
# #         agent_reply = generate_agent_reply(
# #             f"[STRATEGY:{session['strategy_state']}] {payload.latestMessage.text}",
# #             payload.conversationHistory,
# #             session["extracted"]
# #         )
# #     else:
# #         agent_reply = generate_casual_reply(payload.latestMessage.text)

# #     # -----------------------------
# #     # Step 4: FINAL GUVI CALLBACK (MANDATORY)
# #     # -----------------------------
# #     if (
# #         session["scam_detected"]
# #         and not session.get("callback_sent", False)
# #         and (
# #             session["extracted"]["bank_accounts"]
# #             or session["extracted"]["phishing_urls"]
# #             or len(payload.conversationHistory) >= 8
# #         )
# #     ):
# #         send_final_callback(
# #             session_id=payload.sessionId,
# #             scam_detected=True,
# #             total_messages=len(payload.conversationHistory) + 1,
# #             extracted=session["extracted"],
# #             agent_notes="Scammer used urgency and payment redirection tactics"
# #         )
# #         session["callback_sent"] = True

# #     # -----------------------------
# #     # Step 5: Response
# #     # -----------------------------
# #     duration = int(time.time() - session["start_time"])

# #     return HoneypotResponse(
# #         scam_detected=session["scam_detected"],
# #         agent_active=session["scam_detected"],
# #         engagement=EngagementMetrics(
# #             turns=turns,
# #             duration_seconds=duration
# #         ),
# #         extracted_intelligence=ExtractedIntelligence(
# #             upi_ids=list(session["extracted"]["upi_ids"]),
# #             bank_accounts=list(session["extracted"]["bank_accounts"]),
# #             phishing_urls=list(session["extracted"]["phishing_urls"])
# #         ),
# #         agent_reply=agent_reply
# #     )



# # print("MAIN.PY IS RUNNING")
# # import time
# # from fastapi import FastAPI, Depends
# # from app.schemas import (
# #     HoneypotRequest,
# #     HoneypotResponse,
# #     EngagementMetrics,
# #     ExtractedIntelligence
# # )
# # from app.utils import verify_api_key
# # from app.config import APP_NAME
# # from app.gatekeeper import detect_scam
# # from app.memory import get_session
# # from app.extractor import extract_intelligence
# # from app.persona_agent import generate_agent_reply
# # from app.callback import send_final_callback

# # from app.casual_llm import generate_casual_reply

# # app = FastAPI(title=APP_NAME)


# # @app.post("/honeypot", response_model=HoneypotResponse)
# # def honeypot_endpoint(
# #     payload: HoneypotRequest,
# #     _=Depends(verify_api_key)
# # ):
# #     session = get_session(payload.sessionId)
# #     # ---- Strategy State Transition ----
# #     if session["scam_detected"]:
# #         if session["strategy_state"] == "HOOK":
# #             # After first reply → stall
# #             if len(payload.conversationHistory) >= 1:
# #                 session["strategy_state"] = "STALL"
# #     elif session["strategy_state"] == "STALL":
# #         # If no intel yet and enough turns → pivot
# #         if (
# #             len(payload.conversationHistory) >= 2
# #             and not session["extracted"]["upi_ids"]
# #         ):
# #             session["strategy_state"] = "PIVOT"

# #     # Step 1: Scam detection
# #     if not session["scam_detected"]:
# #         session["scam_detected"] = detect_scam(payload.latestMessage.text)

# #     # Step 2: Intelligence extraction
# #     intel = extract_intelligence(payload.latestMessage.text)

# #     for key in intel:
# #         session["extracted"][key].update(intel[key])

# #     # Step 3: Agent reply
# #     turns = len(payload.conversationHistory)
# #     agent_reply = (
# #     generate_agent_reply(
# #         f"[STRATEGY:{session['strategy_state']}] {payload.latestMessage.text}",
# #         payload.conversationHistory,
# #         session["extracted"]
# #     )
# #     if session["scam_detected"]
# #     else generate_casual_reply(payload.latestMessage.text)
# # )

# #     duration = int(time.time() - session["start_time"])
# #     return HoneypotResponse(
# #         scam_detected=session["scam_detected"],
# #     agent_active=session["scam_detected"],
# #     engagement=EngagementMetrics(
# #         turns=turns,
# #         duration_seconds=duration
# #     ),
# #     extracted_intelligence=ExtractedIntelligence(
# #         upi_ids=list(session["extracted"]["upi_ids"]),
# #         bank_accounts=list(session["extracted"]["bank_accounts"]),
# #         phishing_urls=list(session["extracted"]["phishing_urls"])
# #     ),
# #     agent_reply=agent_reply
# # )
# print("MAIN.PY IS RUNNING")

# import time
# from fastapi import FastAPI, Depends

# from app.schemas import (
#     HoneypotRequest,
#     HoneypotResponse,
#     EngagementMetrics,
#     ExtractedIntelligence
# )
# from app.utils import verify_api_key
# from app.config import APP_NAME
# from app.gatekeeper import detect_scam
# from app.memory import get_session
# from app.extractor import extract_intelligence
# from app.persona_agent import generate_agent_reply
# from app.casual_llm import generate_casual_reply
# from app.callback import send_final_callback


# app = FastAPI(title=APP_NAME)


# @app.post("/honeypot", response_model=HoneypotResponse)
# def honeypot_endpoint(
#     payload: HoneypotRequest,
#     _=Depends(verify_api_key)
# ):
#     session = get_session(payload.sessionId)
#     # --- Normalize incoming message (supports tester + swagger) ---
#     incoming = payload.latestMessage or payload.message

#     if not incoming:
#         raise ValueError("No incoming message found")

#     message_text = incoming.text
#     sender_role = incoming.role or incoming.sender or "scammer"

#     # -----------------------------
#     # Strategy State Transition
#     # -----------------------------
#     if session["scam_detected"]:
#         if session["strategy_state"] == "HOOK":
#             if len(payload.conversationHistory) >= 1:
#                 session["strategy_state"] = "STALL"

#         elif session["strategy_state"] == "STALL":
#             if (
#                 len(payload.conversationHistory) >= 2
#                 and not session["extracted"]["upi_ids"]
#             ):
#                 session["strategy_state"] = "PIVOT"

#     # -----------------------------
#     # Step 1: Scam Detection
#     # -----------------------------
#     if not session["scam_detected"]:
#         session["scam_detected"] = detect_scam(message_text)


#     # -----------------------------
#     # Step 2: Intelligence Extraction
#     # -----------------------------
#     intel = extract_intelligence(message_text)

#     for key in intel:
#         session["extracted"][key].update(intel[key])

#     # -----------------------------
#     # Step 3: Agent Reply
#     # -----------------------------
#     turns = len(payload.conversationHistory)

#     if session["scam_detected"]:
#         agent_reply = generate_agent_reply(
#             f"[STRATEGY:{session['strategy_state']}] {message_text}",
#             payload.conversationHistory,
#             session["extracted"]
#         )
#     else:
#         agent_reply = generate_casual_reply(message_text)

#     # -----------------------------
#     # Step 4: FINAL GUVI CALLBACK (MANDATORY)
#     # -----------------------------
#     if (
#         session["scam_detected"]
#         and not session.get("callback_sent", False)
#         and (
#             session["extracted"]["bank_accounts"]
#             or session["extracted"]["phishing_urls"]
#             or len(payload.conversationHistory) >= 8
#         )
#     ):
#         send_final_callback(
#             session_id=payload.sessionId,
#             scam_detected=True,
#             total_messages=len(payload.conversationHistory) + 1,
#             extracted=session["extracted"],
#             agent_notes="Scammer used urgency and payment redirection tactics"
#         )
#         session["callback_sent"] = True

#     # -----------------------------
#     # Step 5: Response
#     # -----------------------------
#     duration = int(time.time() - session["start_time"])

#     return HoneypotResponse(
#         scam_detected=session["scam_detected"],
#         agent_active=session["scam_detected"],
#         engagement=EngagementMetrics(
#             turns=turns,
#             duration_seconds=duration
#         ),
#         extracted_intelligence=ExtractedIntelligence(
#             upi_ids=list(session["extracted"]["upi_ids"]),
#             bank_accounts=list(session["extracted"]["bank_accounts"]),
#             phishing_urls=list(session["extracted"]["phishing_urls"])
#         ),
#         agent_reply=agent_reply
#     )

print("MAIN.PY IS RUNNING")

import time
from fastapi import FastAPI, Depends
#from requests import session
#from app.agent_notes_llm import generate_agent_notes_llm

from app import agent_notes
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
#from app.agent_notes import build_agent_notes
from app.agent_notes_llm import generate_agent_notes_llm

app = FastAPI(title=APP_NAME)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # GUVI tester needs this
    allow_credentials=False,
    allow_methods=["*"],      # VERY IMPORTANT
    allow_headers=["*"],      # VERY IMPORTANT
)
# @app.options("/honeypot")
# def options_honeypot():
#     return {"status": "ok"}

# @app.post("/honeypot", response_model=HoneypotResponse)
@app.post("/honeypot")
def honeypot_endpoint(
    payload: dict
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
        raise ValueError("No incoming message found")

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
            #agent_notes = build_agent_notes(session["extracted"])
            agent_notes=agent_notes

        )
        session["callback_sent"] = True

    # -----------------------------
    # Step 5: Response (GUVI + Extended)
    # -----------------------------
    duration = int(time.time() - session["start_time"])
    #agent_notes = build_agent_notes(session["extracted"])
    return {
    "status": "success",
    "reply": agent_reply,

    "scam_detected": session["scam_detected"],
    "agent_active": session["scam_detected"],

    "engagement": {
        "turns": turns,
        "duration_seconds": duration
    },

    "extracted_intelligence": {
        "upi_ids": list(session["extracted"]["upi_ids"]),
        "bank_accounts": list(session["extracted"]["bank_accounts"]),
        "phishing_urls": list(session["extracted"]["phishing_urls"]),
        "phone_numbers": list(session["extracted"]["phone_numbers"]),
        "emails": list(session["extracted"].get("emails", [])),
        "suspicious_keywords": list(session["extracted"]["suspicious_keywords"]),
        "misc": session["extracted"].get("misc", {})
    },

    "agent_notes": agent_notes
}

#     return HoneypotResponse(
#     status="success",

#     # GUVI-required
#     reply=agent_reply,

#     # internal / extended
#     agent_reply=agent_reply,

#     scam_detected=session["scam_detected"],
#     agent_active=session["scam_detected"],

#     engagement=EngagementMetrics(
#         turns=turns,
#         duration_seconds=duration
#     ),

#     extracted_intelligence=ExtractedIntelligence(
#         upi_ids=list(session["extracted"]["upi_ids"]),
#         bank_accounts=list(session["extracted"]["bank_accounts"]),
#         phishing_urls=list(session["extracted"]["phishing_urls"]),
#         phone_numbers=list(session["extracted"]["phone_numbers"]),
#         emails=list(session["extracted"].get("emails", [])),
#         suspicious_keywords=list(session["extracted"]["suspicious_keywords"]),
#         misc=session["extracted"].get("misc", {})
#     ),

#     agent_notes=agent_notes
# )
@app.get("/")
def health():
    return {"status": "alive"}

@app.options("/{path:path}")
def options_handler(path: str):
    return {"status": "ok"}

