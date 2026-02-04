from pydantic import BaseModel
from typing import List, Optional, Dict

class IncomingMessage(BaseModel):
    sender: str
    text: str
    timestamp: int

class ConversationMessage(BaseModel):
    sender: str
    text: str
    timestamp: int

class HoneypotRequest(BaseModel):
    sessionId: str
    message: IncomingMessage
    conversationHistory: List[ConversationMessage] = []
    metadata: Optional[Dict] = None

class EngagementMetrics(BaseModel):
    turns: int
    duration_seconds: int

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
