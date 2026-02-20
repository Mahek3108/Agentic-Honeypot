


from pydantic import BaseModel
from typing import List, Optional, Dict, Union


class IncomingMessage(BaseModel):
    sender: str
    text: str
    timestamp: Union[int, str]


class ConversationMessage(BaseModel):
    sender: str
    text: str
    timestamp: Union[int, str]


class HoneypotRequest(BaseModel):
    sessionId: str
    message: IncomingMessage
    conversationHistory: List[ConversationMessage] = []
    metadata: Optional[Dict] = None
