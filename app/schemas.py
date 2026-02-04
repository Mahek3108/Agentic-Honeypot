from pydantic import BaseModel, ConfigDict, Field
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
    model_config = ConfigDict(populate_by_name=True)

    turns: int
    duration_seconds: Optional[int] = Field(None, alias="durationSeconds")


class ExtractedIntelligence(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    upi_ids: List[str] = Field(default_factory=list, alias="upiIds")
    bank_accounts: List[str] = Field(default_factory=list, alias="bankAccounts")
    phishing_urls: List[str] = Field(default_factory=list, alias="phishingLinks")
    phone_numbers: List[str] = Field(default_factory=list, alias="phoneNumbers")
    suspicious_keywords: List[str] = Field(default_factory=list, alias="suspiciousKeywords")


class HoneypotResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    status: str
    reply: str

    scam_detected: bool = Field(..., alias="scamDetected")
    agent_active: bool = Field(..., alias="agentActive")

    engagement: EngagementMetrics
    extracted_intelligence: ExtractedIntelligence = Field(..., alias="extractedIntelligence")

    agent_reply: str = Field(..., alias="agentReply")
    agent_notes: str = Field(..., alias="agentNotes")

