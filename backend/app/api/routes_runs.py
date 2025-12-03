"""API routes for sandbox code execution."""
from typing import Dict
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from app.schemas.run import RunCreate, RunResponse
from app.services.sandbox_runner import SandboxRunner
from app.config import settings
from datetime import datetime
import asyncio
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.run import Run as RunModel

router = APIRouter(prefix="/api/runs", tags=["sandbox-runs"])

# In-memory run store (DB persistence can be added later)
runs_store: Dict[str, RunResponse] = {}


@router.post("", response_model=RunResponse, status_code=201)
async def create_run(run_data: RunCreate, db: Session = Depends(get_db)):
    """
    Execute code in an isolated Docker sandbox.
    
    Security features:
    - Non-root user inside container
    - Network disabled by default
    - CPU and memory limits
    - Time-limited execution
    """
    try:
        # Initialize sandbox runner (connects to DinD or local Docker)
        docker_host = getattr(settings, 'DOCKER_HOST', None)
        runner = SandboxRunner(docker_host=docker_host)
        
        # Execute code
        result = await asyncio.to_thread(
            runner.run_in_sandbox,
            language=run_data.language,
            code=run_data.code,
            timeout_sec=run_data.timeout_sec
        )
        
        # Create response
        run_response = RunResponse(
            run_id=result["run_id"],
            language=run_data.language,
            status=result.get("status", "completed"),
            stdout=result.get("stdout", ""),
            stderr=result.get("stderr", ""),
            exit_code=result.get("exit_code", 0),
            execution_time_ms=result.get("execution_time_ms"),
            image=result.get("image"),
            created_at=datetime.utcnow(),
            completed_at=datetime.utcnow()
        )
        
        # Store in memory (for WS demo) and persist in DB
        runs_store[run_response.run_id] = run_response

        db_run = RunModel(
            id=run_response.run_id,
            language=run_response.language,
            status=run_response.status,
            stdout=run_response.stdout,
            stderr=run_response.stderr,
            exit_code=run_response.exit_code,
            image=run_response.image,
            created_at=run_response.created_at,
            completed_at=run_response.completed_at,
        )
        db.add(db_run)
        db.commit()
        
        return run_response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Sandbox execution failed: {str(e)}"
        )


@router.get("/{run_id}", response_model=RunResponse)
async def get_run(run_id: str, db: Session = Depends(get_db)):
    """Get the status and output of a specific run."""
    # Prefer DB record; fallback to in-memory if present
    db_run = db.query(RunModel).filter(RunModel.id == run_id).first()
    if db_run:
        return RunResponse(
            run_id=str(db_run.id),
            language=db_run.language,
            status=db_run.status,
            stdout=db_run.stdout or "",
            stderr=db_run.stderr or "",
            exit_code=db_run.exit_code or 0,
            image=db_run.image,
            created_at=db_run.created_at,
            completed_at=db_run.completed_at,
        )

    run = runs_store.get(run_id)
    if run:
        return run

    raise HTTPException(status_code=404, detail="Run not found")


@router.websocket("/ws/{run_id}/logs")
async def stream_run_logs(websocket: WebSocket, run_id: str):
    """
    Stream live logs from a running sandbox container.
    
    Note: For async execution, this would attach to a running container.
    Current implementation returns stored logs for completed runs.
    """
    await websocket.accept()
    
    try:
        run = runs_store.get(run_id)
        
        if not run:
            await websocket.send_json({"error": "Run not found"})
            await websocket.close()
            return
        
        # Send stored logs
        if run.stdout:
            for line in run.stdout.split('\n'):
                await websocket.send_json({
                    "type": "stdout",
                    "data": line
                })
                await asyncio.sleep(0.01)  # Simulate streaming
        
        if run.stderr:
            for line in run.stderr.split('\n'):
                await websocket.send_json({
                    "type": "stderr",
                    "data": line
                })
                await asyncio.sleep(0.01)
        
        await websocket.send_json({"type": "complete", "status": run.status})
        
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({"error": str(e)})
    finally:
        await websocket.close()
