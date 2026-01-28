from fastapi import APIRouter, HTTPException, BackgroundTasks, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
from pathlib import Path

from core.fixes.registry import FixRegistry
from core.fixes.engine import FixEngine
from core.db import db_instance

# Setup Templates (mirroring main.py logic for now)
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter(prefix="/fixes", tags=["fixes"])

# Request models
class RunFixRequest(BaseModel):
    params: Optional[Dict[str, Any]] = {}

@router.get("/", response_class=HTMLResponse)
async def fixes_dashboard(request: Request):
    """Render the Fixes Dashboard."""
    return templates.TemplateResponse("fixes.html", {"request": request, "title": "Fixes & Repairs"})

@router.get("/api")
async def list_fixes():
    """List all available fixes with their current status."""
    fixes = FixRegistry.get_all_fixes()
    result = []
    for fix in fixes:
        info = FixEngine.get_fix_info(fix.id)
        if info:
            result.append(info)
    return result

@router.get("/history")
async def get_fix_history():
    """Get audit log history."""
    return db_instance.get_history()

@router.get("/{fix_id}")
async def get_fix_details(fix_id: str):
    """Get details for a specific fix."""
    info = FixEngine.get_fix_info(fix_id)
    if not info:
        raise HTTPException(status_code=404, detail="Fix not found")
    return info

@router.post("/{fix_id}/run")
async def run_fix(fix_id: str, request: RunFixRequest, background_tasks: BackgroundTasks):
    """Execute a fix."""
    fix = FixRegistry.get_fix(fix_id)
    if not fix:
        raise HTTPException(status_code=404, detail="Fix not found")

    # If parameters (like PID) are needed, set them
    if fix_id == "terminate_process" and "pid" in request.params:
        try:
             fix.set_target(int(request.params["pid"]))
        except ValueError:
             raise HTTPException(status_code=400, detail="Invalid PID")

    # Run the fix via the engine
    result = FixEngine.run_fix(fix_id)
    return result


