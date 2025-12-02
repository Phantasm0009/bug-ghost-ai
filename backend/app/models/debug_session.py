"""DebugSession database model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.db.session import Base


class SessionStatus(str, enum.Enum):
    """Status of a debug session."""
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class DebugSession(Base):
    """Debug session model."""
    
    __tablename__ = "debug_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Input data
    language = Column(String(50), nullable=False)
    runtime_info = Column(String(200), nullable=True)
    error_text = Column(Text, nullable=False)
    code_snippet = Column(Text, nullable=True)
    context_description = Column(Text, nullable=True)
    
    # Status
    status = Column(Enum(SessionStatus), default=SessionStatus.PROCESSING, nullable=False)
    
    # Generated outputs
    repro_code = Column(Text, nullable=True)
    test_code = Column(Text, nullable=True)
    explanation = Column(Text, nullable=True)
    fix_suggestion = Column(Text, nullable=True)
    
    # Metadata
    llm_model = Column(String(100), nullable=True)
    error_message = Column(Text, nullable=True)  # For internal failures
    
    def __repr__(self):
        return f"<DebugSession(id={self.id}, language={self.language}, status={self.status})>"
