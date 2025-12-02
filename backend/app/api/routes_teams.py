"""Basic team collaboration endpoints."""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.team import Team, Membership, TeamRole
from app.models.user import User
from pydantic import BaseModel, Field
from typing import Optional, List
import re

router = APIRouter(prefix="/api/teams", tags=["teams"]) 


def slugify(name: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", name.strip()).strip("-")
    return s.lower() or "team"


class TeamCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    owner_user_id: Optional[str] = None


class AddMember(BaseModel):
    user_id: str
    role: TeamRole = TeamRole.member


@router.post("", response_model=dict)
def create_team(payload: TeamCreate, db: Session = Depends(get_db)):
    slug = slugify(payload.name)
    existing = db.query(Team).filter(Team.slug == slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Team with this name already exists")
    team = Team(name=payload.name, slug=slug)
    db.add(team)
    db.commit()
    db.refresh(team)

    if payload.owner_user_id:
        db.add(Membership(user_id=payload.owner_user_id, team_id=team.id, role=TeamRole.owner))
        db.commit()

    return {"id": str(team.id), "name": team.name, "slug": team.slug}


@router.get("", response_model=List[dict])
def list_teams(user_id: Optional[str] = None, db: Session = Depends(get_db)):
    if user_id:
        rows = (
            db.query(Team)
            .join(Membership, Membership.team_id == Team.id)
            .filter(Membership.user_id == user_id)
            .all()
        )
    else:
        rows = db.query(Team).all()
    return [{"id": str(t.id), "name": t.name, "slug": t.slug} for t in rows]


@router.post("/{team_id}/members", response_model=dict)
def add_member(team_id: str, payload: AddMember, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    existing = (
        db.query(Membership)
        .filter(Membership.team_id == team_id, Membership.user_id == payload.user_id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="User already a member")

    m = Membership(team_id=team_id, user_id=payload.user_id, role=payload.role)
    db.add(m)
    db.commit()
    return {"team_id": team_id, "user_id": payload.user_id, "role": m.role}
