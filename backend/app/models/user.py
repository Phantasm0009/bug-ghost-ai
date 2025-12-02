"""User model for GitHub OAuth authenticated users."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    github_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    name = Column(String(200), nullable=True)
    avatar_url = Column(String(500), nullable=True)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, github_id={self.github_id}, username={self.username})>"
