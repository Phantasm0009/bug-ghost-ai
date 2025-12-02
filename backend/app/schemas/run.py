"""Schemas for sandbox run requests and responses."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class RunCreate(BaseModel):
    """Request to create a new sandbox run."""
    language: str = Field(..., description="Programming language (python, javascript, typescript, java, etc.)")
    code: str = Field(..., description="Code to execute in the sandbox")
    timeout_sec: int = Field(default=10, ge=1, le=60, description="Timeout in seconds (1-60)")


class RunResponse(BaseModel):
    """Response from creating or getting a run."""
    run_id: str
    language: str
    status: str  # pending, running, completed, error, timeout
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    exit_code: Optional[int] = None
    error: Optional[str] = None
    image: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
