from pydantic import BaseModel
from typing import List, Optional, Dict, Union


class IncomingMessage(BaseModel):
    sender: Optional[str] = "user"
    role: Optional[str] = None
    text: str
    timestamp: Optional[Union[int, str, float]] = None


class ConversationMessage(BaseModel):
    sender: Optional[str] = "user"
    role: Optional[str] = None
    text: str
    timestamp: Optional[Union[int, str, float]] = None


class HoneypotRequest(BaseModel):
    sessionId: str

    # GUVI MAY SEND EITHER
    message: Optional[IncomingMessage] = None
    latestMessage: Optional[IncomingMessage] = None

    conversationHistory: List[ConversationMessage] = []
    metadata: Optional[Dict] = None


class EngagementMetrics(BaseModel):
    turns: int
    duration_seconds: Optional[int] = None


class ExtractedIntelligence(BaseModel):
    upi_ids: List[str] = []
    bank_accounts: List[str] = []
    phishing_urls: List[str] = []
    phone_numbers: List[str] = []
    suspicious_keywords: List[str] = []


class HoneypotResponse(BaseModel):
    status: str
    reply: str

    scam_detected: bool
    agent_active: bool

    engagement: EngagementMetrics
    extracted_intelligence: ExtractedIntelligence

    agent_reply: str
    agent_notes: str
