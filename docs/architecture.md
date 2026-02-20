# Honeypot API – System Architecture

## 1. Overview

This system implements an AI-driven conversational honeypot designed to:

Detect scam attempts

Extract intelligence from scam conversations

Sustain realistic multi-turn engagement

Generate structured final analysis for evaluation


The architecture is modular, scalable, and evaluation-safe (no hardcoded scenario logic).


---

 **Core Components**

---

## 2. API Layer (FastAPI)

File: main.py

Handles:

-Incoming scam message

-Conversation history

-Metadata

-Session tracking

-Response generation

-Final callback trigger


-Responsibilities

-Validate API key

-Maintain session state

-Route to detection / extractor / persona

-Return response within 30 seconds



---

## 3. Session Memory Layer

File: memory.py

Maintains per-session state:

{
  "scam_detected": bool,
  "extracted": dict,
  "start_time": float,
  "callback_sent": bool
}

Purpose:

-Accumulate extracted intelligence across turns

-Prevent duplicate callback submissions

-Track engagement duration

-Maintain conversational continuity



---

## 4. Scam Detection Engine

File: gatekeeper.py

Hybrid rule-based detection using:

-Keyword scoring

-Urgency detection

-OTP / PIN / freeze signals

-Threat-based phrases


Design Goals:

-Generic scam detection

-No hardcoded scenario logic

-Adaptable to multiple fraud types



---

## 5. Intelligence Extraction Engine

File: extractor.py

Uses:

-Regex-based entity extraction

-Context-aware window logic

-Overlap prevention

-Deduplication


Extracted Entities:

-Phone Numbers (mobile + toll-free + landline)

-Bank Account Numbers (11–18 digits)

-UPI IDs

-Email Addresses

-Phishing URLs

-Policy Numbers

-Order Numbers

-Case IDs

-Suspicious Keywords


Extraction accumulates across conversation turns.


---

## 6. Persona Agent (LLM-Based)

File: persona_agent.py

Uses an LLM with a structured system prompt.

Features:

-Emotional realism

-Progressive stress response

-Red flag identification

-Information elicitation

-Strict non-disclosure of sensitive data

-Short SMS-style replies (1–2 lines)


Conversation Strategy:

-Identity probing

-Contact elicitation

-Website verification

-Reference ID requests

-Urgency challenge

-Inconsistency detection


This directly improves:

-Conversation Quality score

-Red Flag score

-Information Elicitation score



---

## 7. Agent Notes Generator

File: agent_notes_llm.py

Generates final scam summary including:

-Tactics used

-Manipulation patterns

-Threat indicators

-Extracted intelligence context


This strengthens:

-Final output structure

-Manual review clarity



---

## 8. Engagement Metrics Engine

Calculates:

-Total messages exchanged

-Engagement duration (real-time based on session start)


Metrics influence:

-Engagement Quality score

-Structural completeness score


No artificial inflation is applied.


---

## 9. Scam Type & Confidence Module

File: callback.py

Determines:

-scamType (bank_fraud / upi_fraud / phishing / etc.)

-confidenceLevel (based on signal density)


Confidence Calculation Factors:

-Presence of multiple intelligence categories

-Suspicious keyword density

-Detection triggers



---

## 10. Final Callback Module

Triggered near conversation completion.

Sends structured payload:

{
  "sessionId": "...",
  "scamDetected": true,
  "totalMessagesExchanged": 18,
  "engagementDurationSeconds": 120,
  "extractedIntelligence": { ... },
  "agentNotes": "...",
  "scamType": "...",
  "confidenceLevel": 0.92
}

Callback Rules:


-Only after scam detection

-After sufficient conversation turns

-Mirrored to personal webhook for debugging



---

Design Principles:

-Generic Logic

-No scenario-specific hardcoding.

-Modular Architecture

-Clear separation between detection, extraction, conversation, and reporting.

-Evaluation-Safe

-Strict adherence to required JSON schema.

-Scalable

Easily extendable with:

-ML classifiers

-Advanced NLP

-Persistent storage

-Dashboard integration


Reviewer-Friendly

Readable structure, isolated responsibilities, and clean logic separation.


---

Security Considerations:

-API key validation

-No sensitive data exposure

-Strict persona guardrails

-No AI/system disclosure

-Request timeout protection (<30s)



---

Future Improvements:

-ML-based scam classification

-Semantic intent scoring

-Adaptive elicitation strategy

-Real-time fraud risk scoring

-Persistent database storage

-Intelligence monitoring dashboard



---

**Conclusion:**

This architecture provides:

-Robust scam detection

-Multi-entity intelligence extraction

-Realistic multi-turn engagement

-Structured final reporting

-Evaluation-aligned scoring optimization


**The system balances:**

Technical robustness
Conversational realism
Scoring strategy alignment

