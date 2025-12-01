from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
from dotenv import load_dotenv
import openai

load_dotenv()

app = FastAPI(
    title="Vapi Custom LLM Server",
    description="Custom LLM server for Vapi integration using FastAPI",
    version="1.0.0"
)

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY", "")

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

@app.post("/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(
    request: ChatCompletionRequest,
    authorization: Optional[str] = Header(None)
):
    """
    Vapi Custom LLM endpoint for chat completions.
    
    This endpoint receives conversation context from Vapi and returns
    LLM-generated responses formatted according to Vapi's specification.
    
    Headers:
        authorization: Optional API key for authentication (if configured in Vapi)
    """
    try:
        # Optional: Validate API key if provided
        if authorization:
            expected_key = os.getenv("VAPI_API_KEY", "")
            if expected_key and not authorization.startswith(f"Bearer {expected_key}"):
                raise HTTPException(status_code=401, detail="Unauthorized")
        
        # Build messages list
        messages = []
        
        # Add system prompt if provided
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        
        # Add conversation history
        for msg in request.messages:
            messages.append({"role": msg.role, "content": msg.content})
        
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model=request.model,
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        
        # Format response according to Vapi's expected structure
        return ChatCompletionResponse(
            choices=[{
                "message": {
                    "role": "assistant",
                    "content": response.choices[0].message.content
                },
                "finish_reason": response.choices[0].finish_reason
            }],
            model=response.model,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "service": "vapi-custom-llm"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
