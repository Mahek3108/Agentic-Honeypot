from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any, Union


class IncomingMessage(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    sender: str
    text: str
    timestamp: Union[int, str, float]


class HoneypotRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    sessionId: str
    message: IncomingMessage
    conversationHistory: List[Dict[str, Any]] = []
    metadata: Optional[Dict[str, Any]] = None


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

