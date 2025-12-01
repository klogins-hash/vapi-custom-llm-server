from fastapi import FastAPI, HTTPException, Header, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
import os
from dotenv import load_dotenv
import openai

from database import init_db, get_db, LLMInteraction
from models import ChatCompletionRequest, ChatCompletionResponse, InteractionResponse, Message

load_dotenv()

app = FastAPI(
    title="Vapi Custom LLM Server",
    description="Custom LLM server for Vapi integration using FastAPI with database support",
    version="1.0.0"
)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    """Initialize database on application startup"""
    init_db()
    openai.api_key = os.getenv("OPENAI_API_KEY", "")

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY", "")

@app.post("/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(
    request: ChatCompletionRequest,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Vapi Custom LLM endpoint for chat completions.

    This endpoint receives conversation context from Vapi and returns
    LLM-generated responses formatted according to Vapi's specification.
    Interactions are logged to the database.

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
        user_message = None

        # Add system prompt if provided
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})

        # Add conversation history and capture last user message
        for msg in request.messages:
            messages.append({"role": msg.role, "content": msg.content})
            if msg.role == "user":
                user_message = msg.content

        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model=request.model,
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        assistant_response = response.choices[0].message.content
        total_tokens = response.usage.total_tokens

        # Log interaction to database
        try:
            interaction = LLMInteraction(
                user_message=user_message or "System message",
                assistant_response=assistant_response,
                model=request.model,
                temperature=request.temperature,
                tokens_used=total_tokens
            )
            db.add(interaction)
            db.commit()
        except Exception as db_error:
            print(f"Database logging error: {db_error}")
            # Don't fail the request if database logging fails
            db.rollback()

        # Format response according to Vapi's expected structure
        return ChatCompletionResponse(
            choices=[{
                "message": {
                    "role": "assistant",
                    "content": assistant_response
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
    except HTTPException:
        raise
    except Exception as e:
        # Log error to database
        try:
            interaction = LLMInteraction(
                user_message=request.messages[-1].content if request.messages else "Unknown",
                assistant_response=None,
                model=request.model,
                temperature=request.temperature,
                tokens_used=0,
                error_message=str(e)
            )
            db.add(interaction)
            db.commit()
        except:
            db.rollback()

        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "service": "vapi-custom-llm"}

@app.get("/interactions", response_model=List[InteractionResponse])
async def get_interactions(
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Get recent LLM interactions from database"""
    interactions = db.query(LLMInteraction).order_by(
        LLMInteraction.created_at.desc()
    ).offset(offset).limit(limit).all()
    return interactions

@app.get("/interactions/stats")
async def get_interaction_stats(db: Session = Depends(get_db)):
    """Get statistics about LLM interactions"""
    total = db.query(LLMInteraction).count()
    total_tokens = db.query(func.sum(LLMInteraction.tokens_used)).scalar() or 0

    return {
        "total_interactions": total,
        "total_tokens_used": total_tokens,
        "average_tokens_per_interaction": total_tokens // total if total > 0 else 0
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
