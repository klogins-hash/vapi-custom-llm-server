import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Database URL configuration
# For SQLite: Use mounted volume at /app/data for persistence
# For PostgreSQL: Use DATABASE_URL environment variable (auto-injected by Railway)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:////app/data/vapi_custom_llm.db"
)

# Handle PostgreSQL connection string format from Railway
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    # Convert postgresql:// to postgresql+psycopg2://
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class LLMInteraction(Base):
    """Store LLM interaction logs"""
    __tablename__ = "llm_interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(Text, nullable=False)
    assistant_response = Column(Text, nullable=True)
    model = Column(String(255), default="gpt-3.5-turbo")
    temperature = Column(Float, default=0.7)
    tokens_used = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create all tables
def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
