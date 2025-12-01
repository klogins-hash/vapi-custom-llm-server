from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    messages: List[Message]
    model: Optional[str] = "gpt-3.5-turbo"
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1000
    system_prompt: Optional[str] = None

class ChatCompletionResponse(BaseModel):
    choices: List[Dict[str, Any]]
    model: str
    usage: Dict[str, int]

class InteractionResponse(BaseModel):
    id: int
    user_message: str
    assistant_response: Optional[str] = None
    model: str
    tokens_used: int
    created_at: datetime

    class Config:
        from_attributes = True
