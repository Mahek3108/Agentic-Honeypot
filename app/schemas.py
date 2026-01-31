from pydantic import BaseModel
from typing import List, Optional, Dict


# ----------------------------
# Incoming Messages
# ----------------------------

class IncomingMessage(BaseModel):
    # Supports BOTH:
    # - your swagger format (role)
    # - GUVI tester format (sender)
    role: Optional[str] = None
    sender: Optional[str] = None
    text: str
    timestamp: Optional[int | str] = None


class ConversationMessage(BaseModel):
    role: Optional[str] = None
    sender: Optional[str] = None
    text: str
    timestamp: Optional[int | str] = None


# ----------------------------
# Request Schema
# ----------------------------

class HoneypotRequest(BaseModel):
    sessionId: str
    latestMessage: Optional[IncomingMessage] = None   # swagger/local
    message: Optional[IncomingMessage] = None         # GUVI tester
    conversationHistory: List[ConversationMessage] = []
    metadata: Optional[Dict] = None


# ----------------------------
# Response Sub-Schemas
# ----------------------------

class EngagementMetrics(BaseModel):
    turns: int
    duration_seconds: Optional[int] = None


class ExtractedIntelligence(BaseModel):
    # INTERNAL + visible in response
    upi_ids: List[str] = []
    bank_accounts: List[str] = []
    phishing_urls: List[str] = []
    phone_numbers: List[str] = []
    emails: List[str] = []
    suspicious_keywords: List[str] = []
    misc: Dict = {}


# ----------------------------
# FINAL RESPONSE SCHEMA
# ----------------------------

class HoneypotResponse(BaseModel):
    # 🔹 GUVI-required fields
    status: str                    # always "success"
    reply: str                     # SAME as agent_reply

    # 🔹 Your internal evaluation fields
    scam_detected: bool
    agent_active: bool
    engagement: EngagementMetrics
    extracted_intelligence: ExtractedIntelligence

    # 🔹 Keep for debugging / parity
    agent_reply: str
    agent_notes: str