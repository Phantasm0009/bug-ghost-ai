"""Pydantic schemas for debug sessions."""
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from app.models.debug_session import SessionStatus


class DebugSessionCreate(BaseModel):
    """Schema for creating a new debug session."""
    
    language: str = Field(..., min_length=1, max_length=50, description="Programming language")
    runtime_info: Optional[str] = Field(None, max_length=200, description="Runtime information (e.g., Node 18, Python 3.11)")
    error_text: str = Field(..., min_length=1, description="Error message or stack trace")
    code_snippet: Optional[str] = Field(None, description="Relevant code snippet")
    context_description: Optional[str] = Field(None, description="Additional context about when the error occurs")


class ReproductionResult(BaseModel):
    """Result from LLM reproduction generation."""
    
    repro_code: str
    test_code: str
    explanation: str
    fix_suggestion: str


class DebugSessionResponse(BaseModel):
    """Response schema for a debug session."""
    
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    # Input
    language: str
    runtime_info: Optional[str]
    error_text: str
    code_snippet: Optional[str]
    context_description: Optional[str]
    
    # Status
    status: SessionStatus
    
    # Output
    repro_code: Optional[str]
    test_code: Optional[str]
    explanation: Optional[str]
    fix_suggestion: Optional[str]
    
    # Metadata
    llm_model: Optional[str]
    error_message: Optional[str]
    
    class Config:
        from_attributes = True


class DebugSessionListResponse(BaseModel):
    """Response schema for listing debug sessions."""
    
    id: UUID
    created_at: datetime
    language: str
    error_snippet: str  # First line of error
    status: SessionStatus
    
    class Config:
        from_attributes = True
