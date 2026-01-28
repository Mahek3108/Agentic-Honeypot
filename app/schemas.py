
from pydantic import BaseModel
from typing import List, Optional


class Message(BaseModel):
    role: str   # "scammer" | "agent"
    text: str


class HoneypotRequest(BaseModel):
    sessionId: str
    latestMessage: Message
    conversationHistory: List[Message]


class ExtractedIntelligence(BaseModel):
    upi_ids: List[str] = []
    bank_accounts: List[str] = []
    phishing_urls: List[str] = []


class EngagementMetrics(BaseModel):
    turns: int
    duration_seconds: Optional[int] = None


class HoneypotResponse(BaseModel):
    scam_detected: bool
    agent_active: bool
    engagement: EngagementMetrics
    extracted_intelligence: ExtractedIntelligence
    agent_reply: str
