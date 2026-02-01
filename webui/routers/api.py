from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from typing import Dict, Any, Optional, List
from io import BytesIO
from pydantic import BaseModel

from diagnostics import DIAGNOSTIC_FUNCTIONS
from core.fixes.engine import FixEngine
from core.fixes.registry import FixRegistry
from core.db import db_instance
from core.history import HistoryTracker
from core.reports import ReportGenerator
from core.auth import require_api_key

router = APIRouter(prefix="/api/v1", tags=["api"])

class RunFixRequest(BaseModel):
    params: Optional[Dict[str, Any]] = None


@router.get("/diagnostics", dependencies=[Depends(require_api_key)])
def list_diagnostics() -> List[Dict[str, str]]:
    return [{"id": key} for key in DIAGNOSTIC_FUNCTIONS.keys()]


@router.post("/diagnostics/{tool_id}", dependencies=[Depends(require_api_key)])
def run_diagnostic(tool_id: str) -> Dict[str, Any]:
    func = DIAGNOSTIC_FUNCTIONS.get(tool_id)
    if not func:
        raise HTTPException(status_code=404, detail="Diagnostic not found")
    output = func()
    return {"id": tool_id, "output": output}


@router.get("/fixes", dependencies=[Depends(require_api_key)])
def list_fixes() -> List[Dict[str, Any]]:
    return FixEngine.get_all_fix_info()


@router.post("/fixes/{fix_id}", dependencies=[Depends(require_api_key)])
def run_fix(fix_id: str, payload: RunFixRequest = RunFixRequest()) -> Dict[str, Any]:
    fix = FixRegistry.get_fix(fix_id)
    if not fix:
        raise HTTPException(status_code=404, detail="Fix not found")

    if fix_id == "terminate_process" and payload.params and "pid" in payload.params:
        try:
            fix.set_target(int(payload.params["pid"]))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid PID")

    return FixEngine.run_fix(fix_id)


@router.get("/history", dependencies=[Depends(require_api_key)])
def get_history() -> List[Dict[str, Any]]:
    return db_instance.get_history()


@router.get("/health", dependencies=[Depends(require_api_key)])
def get_health() -> Dict[str, Any]:
    return HistoryTracker.collect_snapshot()


@router.get("/report/pdf", dependencies=[Depends(require_api_key)])
def get_report_pdf(
    report_type: str = Query("health", pattern="^(diagnostic|fixes|health)$"),
    tool_id: Optional[str] = None,
):
    if report_type == "diagnostic":
        tool = tool_id or "system_overview"
        func = DIAGNOSTIC_FUNCTIONS.get(tool)
        if not func:
            raise HTTPException(status_code=404, detail="Diagnostic not found")
        content = func()
        pdf_bytes = ReportGenerator.generate_diagnostic_report(content)
        filename = f"diagnostix_diagnostic_{tool}.pdf"
    elif report_type == "fixes":
        history = db_instance.get_history()
        pdf_bytes = ReportGenerator.generate_fix_summary(history)
        filename = "diagnostix_fix_summary.pdf"
    else:
        metrics = HistoryTracker.collect_snapshot()
        pdf_bytes = ReportGenerator.generate_system_health_report(metrics)
        filename = "diagnostix_system_health.pdf"

    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
