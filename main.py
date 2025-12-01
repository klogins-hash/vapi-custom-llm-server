from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Vapi Custom LLM",
    description="Custom LLM server for Vapi integration",
    version="1.0.0"
)

class MessageRequest(BaseModel):
    message: str
    system_prompt: Optional[str] = None

class MessageResponse(BaseModel):
    response: str
    success: bool

@app.post("/v1/message", response_model=MessageResponse)
async def handle_message(request: MessageRequest):
    """Custom LLM endpoint for Vapi"""
    try:
        # TODO: Integrate your LLM here
        # This is a placeholder for custom LLM logic
        response = f"Echo: {request.message}"
        return MessageResponse(response=response, success=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
