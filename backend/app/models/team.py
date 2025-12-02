"""Team and Membership models for collaboration."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from app.db.session import Base


class TeamRole(str, enum.Enum):
    owner = "owner"
    admin = "admin"
    member = "member"


class Team(Base):
    __tablename__ = "teams"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    name = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)

    memberships = relationship("Membership", back_populates="team", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Team(id={self.id}, slug={self.slug})>"


class Membership(Base):
    __tablename__ = "memberships"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    role = Column(Enum(TeamRole), default=TeamRole.member, nullable=False)

    team = relationship("Team", back_populates="memberships")

    __table_args__ = (
        UniqueConstraint('user_id', 'team_id', name='uq_user_team'),
    )

    def __repr__(self) -> str:
        return f"<Membership(user_id={self.user_id}, team_id={self.team_id}, role={self.role})>"
