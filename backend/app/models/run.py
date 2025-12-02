"""Run history database model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.db.session import Base


class Run(Base):
    """Represents a sandbox code execution run."""

    __tablename__ = "runs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)

    language = Column(String(50), nullable=False)
    status = Column(String(32), nullable=False)
    stdout = Column(Text, nullable=True)
    stderr = Column(Text, nullable=True)
    exit_code = Column(Integer, nullable=True)
    image = Column(String(200), nullable=True)

    def __repr__(self) -> str:
        return f"<Run(id={self.id}, language={self.language}, status={self.status})>"
