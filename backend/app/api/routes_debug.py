"""API routes for debug sessions."""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.debug_session import DebugSession, SessionStatus
from app.schemas.debug_session import (
    DebugSessionCreate,
    DebugSessionResponse,
    DebugSessionListResponse
)
from app.services.llm_client import LLMClient
from app.services.repro_generator import ReproductionGenerator
from app.config import settings

router = APIRouter(prefix="/api/debug-sessions", tags=["debug-sessions"])


@router.post("", response_model=DebugSessionResponse, status_code=201)
async def create_debug_session(
    session_data: DebugSessionCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new debug session and generate reproduction.
    
    This endpoint:
    1. Creates a session with status=processing
    2. Calls LLM to generate reproduction, test, explanation, and fix
    3. Updates session with results
    4. Returns complete session
    """
    
    # Create initial session
    db_session = DebugSession(
        language=session_data.language,
        runtime_info=session_data.runtime_info,
        error_text=session_data.error_text,
        code_snippet=session_data.code_snippet,
        context_description=session_data.context_description,
        status=SessionStatus.PROCESSING
    )
    
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    
    try:
        # Create LLM client
        llm_client = LLMClient.create(
            provider=settings.LLM_PROVIDER,
            api_key=settings.LLM_API_KEY,
            model=settings.LLM_MODEL
        )
        
        # Generate reproduction
        generator = ReproductionGenerator(llm_client)
        result = await generator.generate_reproduction(session_data)
        
        # Update session with results
        db_session.repro_code = result.repro_code
        db_session.test_code = result.test_code
        db_session.explanation = result.explanation
        db_session.fix_suggestion = result.fix_suggestion
        db_session.llm_model = settings.LLM_MODEL
        db_session.status = SessionStatus.COMPLETED
        
        db.commit()
        db.refresh(db_session)
        
    except Exception as e:
        # Mark as failed
        db_session.status = SessionStatus.FAILED
        db_session.error_message = str(e)
        db.commit()
        db.refresh(db_session)
        
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate reproduction: {str(e)}"
        )
    
    return db_session


@router.get("/{session_id}", response_model=DebugSessionResponse)
async def get_debug_session(session_id: UUID, db: Session = Depends(get_db)):
    """Get a specific debug session by ID."""
    
    db_session = db.query(DebugSession).filter(DebugSession.id == session_id).first()
    
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return db_session


@router.get("", response_model=List[DebugSessionListResponse])
async def list_debug_sessions(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """List debug sessions with pagination."""
    
    sessions = db.query(DebugSession)\
        .order_by(DebugSession.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    # Transform to list response
    return [
        DebugSessionListResponse(
            id=session.id,
            created_at=session.created_at,
            language=session.language,
            error_snippet=session.error_text.split('\n')[0][:100],
            status=session.status
        )
        for session in sessions
    ]
