"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.routes_debug import router as debug_router
from app.api.routes_runs import router as runs_router
from app.db.session import engine, Base
# Ensure models are imported before create_all
from app.models import run as _run_model  # noqa: F401
from app.models import user as _user_model  # noqa: F401
from app.models import team as _team_model  # noqa: F401

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bug Ghost AI",
    description="AI Debug Replayer - Transform errors into reproducible bug scenarios",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
from app.api.routes_auth import router as auth_router
from app.api.routes_teams import router as teams_router
from app.api.routes_sandbox import router as sandbox_router

app.include_router(debug_router)
app.include_router(runs_router)
app.include_router(auth_router)
app.include_router(teams_router)
app.include_router(sandbox_router)


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "name": "Bug Ghost AI",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
