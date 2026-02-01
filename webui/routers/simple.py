from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import Dict, List, Any
from uuid import uuid4
import json
import time

from core.fixes.registry import FixRegistry
from core.fixes.engine import FixEngine
from core.fixes.base import RiskLevel

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter(prefix="/simple", tags=["simple"])

# Wizard copy and fix mapping are explicit to keep Simple Mode behavior auditable.
ISSUE_OPTIONS = [
    {"id": "network", "label": "Internet or network problems"},
    {"id": "slow", "label": "Computer feels slow"},
    {"id": "boot", "label": "Startup or boot issues"},
    {"id": "security", "label": "Security or integrity check"},
    {"id": "cleanup", "label": "General cleanup"},
]

WIZARD_FIX_MAP: Dict[str, List[str]] = {
    # Network problems
    "network": [
        "flush_dns",
        "restart_network",
        "network_adapter_diagnostics",
    ],
    # Feels slow
    "slow": [
        "clear_temp_files",
        "clear_pip_cache",
        "disable_bloat_services",
        "power_performance",
    ],
    # Startup or boot
    "boot": [
        "startup_analysis",
        "ram_test",
    ],
    # Security / integrity
    "security": [
        "port_scan",
        "system_snapshot",
    ],
    # General cleanup
    "cleanup": [
        "clear_temp_files",
        "clear_pip_cache",
        "clean_temp_advanced",
    ],
}

ACTION_LABELS: Dict[str, str] = {
    "clear_temp_files": "Clear temporary files to free up space.",
    "clear_pip_cache": "Remove old app caches to reclaim space.",
    "flush_dns": "Refresh network name lookups to fix connection glitches.",
    "restart_network": "Restart network services to restore connectivity.",
    "network_adapter_diagnostics": "Check your network connections and build a report.",
    "disable_bloat_services": "Turn off background services you do not need.",
    "power_performance": "Set your computer to prioritize speed over power saving.",
    "startup_analysis": "Show programs that start automatically with your computer.",
    "ram_test": "Schedule a memory test to check for hardware issues.",
    "port_scan": "Check which network ports are open on your computer.",
    "system_snapshot": "Create a system health report for troubleshooting.",
    "clean_temp_advanced": "Deep clean temporary files and leftover junk.",
}

# Fixes that require user-supplied input are blocked from Simple Mode.
BLOCKED_FIXES = {
    "terminate_process",
    "kill_process_advanced",
    "file_hash",
}

# In-memory run state keyed by Simple Mode session id.
_RUN_STATE: Dict[str, Dict[str, Any]] = {}


def _get_session_id(request: Request) -> str:
    session_id = request.session.get("simple_session_id")
    if not session_id:
        session_id = uuid4().hex
        request.session["simple_session_id"] = session_id
    return session_id


def _reset_wizard_state(request: Request) -> None:
    for key in ("simple_issue", "simple_risk", "simple_plan"):
        request.session.pop(key, None)
    session_id = _get_session_id(request)
    _RUN_STATE.pop(session_id, None)


def _dedupe_keep_order(items: List[str]) -> List[str]:
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def _build_plan(issue_id: str, risk_mode: str) -> List[str]:
    if risk_mode not in ("safe", "moderate"):
        risk_mode = "safe"
    fix_ids = _dedupe_keep_order(WIZARD_FIX_MAP.get(issue_id, []))
    plan: List[str] = []
    for fix_id in fix_ids:
        if fix_id in BLOCKED_FIXES:
            continue
        fix = FixRegistry.get_fix(fix_id)
        if not fix:
            continue
        if not fix.check_platform_compatibility():
            continue
        if fix.risk_level == RiskLevel.DANGEROUS:
            continue
        if risk_mode == "safe" and fix.risk_level != RiskLevel.SAFE:
            continue
        plan.append(fix_id)
    return plan


def _action_label_for(fix_id: str) -> str:
    if fix_id in ACTION_LABELS:
        return ACTION_LABELS[fix_id]
    fix = FixRegistry.get_fix(fix_id)
    if fix:
        return fix.get_simple_description()
    return "Recommended system action."


def _format_details(result: Dict[str, Any]) -> str:
    details = result.get("details")
    if details is None:
        details = {k: v for k, v in result.items() if k not in ("success", "message", "skipped")}
    try:
        text = json.dumps(details, indent=2, ensure_ascii=True)
    except TypeError:
        text = str(details)
    if len(text) > 8000:
        text = text[:8000] + "\n...\n"
    return text


def _friendly_message(status: str) -> str:
    if status == "success":
        return "Completed."
    if status == "skipped":
        return "Nothing needed."
    return "Could not complete this step."


def _issue_label(issue_id: str) -> str:
    for option in ISSUE_OPTIONS:
        if option["id"] == issue_id:
            return option["label"]
    return "Selected issue"


@router.get("/", response_class=HTMLResponse)
async def simple_step1(request: Request):
    _reset_wizard_state(request)
    return templates.TemplateResponse(
        request,
        "simple/step1.html",
        {
            "title": "Simple Mode",
            "options": ISSUE_OPTIONS,
        },
    )


@router.post("/step1")
async def simple_step1_submit(request: Request, issue: str = Form(...)):
    option_ids = {option["id"] for option in ISSUE_OPTIONS}
    if issue not in option_ids:
        raise HTTPException(status_code=400, detail="Invalid selection")
    request.session["simple_issue"] = issue
    return RedirectResponse("/simple/step2", status_code=303)


@router.get("/step2", response_class=HTMLResponse)
async def simple_step2(request: Request):
    issue = request.session.get("simple_issue")
    if not issue:
        return RedirectResponse("/simple", status_code=303)
    selected = request.session.get("simple_risk", "safe")
    return templates.TemplateResponse(
        request,
        "simple/step2.html",
        {
            "title": "Simple Mode",
            "selected": selected,
            "issue_label": _issue_label(issue),
            "show_warning": False,
        },
    )


@router.post("/step2", response_class=HTMLResponse)
async def simple_step2_submit(
    request: Request,
    risk: str = Form(...),
    confirm: str = Form(None),
):
    if risk not in ("safe", "moderate"):
        raise HTTPException(status_code=400, detail="Invalid selection")
    if risk == "moderate" and confirm != "yes":
        request.session["simple_risk"] = risk
        return templates.TemplateResponse(
            request,
            "simple/step2.html",
            {
                "title": "Simple Mode",
                "selected": risk,
                "issue_label": _issue_label(request.session.get("simple_issue", "")),
                "show_warning": True,
            },
        )
    request.session["simple_risk"] = risk
    return RedirectResponse("/simple/step3", status_code=303)


@router.get("/step3", response_class=HTMLResponse)
async def simple_step3(request: Request):
    issue = request.session.get("simple_issue")
    if not issue:
        return RedirectResponse("/simple", status_code=303)
    risk = request.session.get("simple_risk", "safe")
    plan = _build_plan(issue, risk)
    request.session["simple_plan"] = plan
    actions = [_action_label_for(fix_id) for fix_id in plan]
    return templates.TemplateResponse(
        request,
        "simple/step3.html",
        {
            "title": "Simple Mode",
            "issue_label": _issue_label(issue),
            "risk": risk,
            "actions": actions,
            "has_actions": len(actions) > 0,
        },
    )


@router.post("/run")
async def simple_run_start(request: Request):
    issue = request.session.get("simple_issue")
    if not issue:
        return RedirectResponse("/simple", status_code=303)
    risk = request.session.get("simple_risk", "safe")
    plan = request.session.get("simple_plan")
    if not isinstance(plan, list):
        plan = _build_plan(issue, risk)
        request.session["simple_plan"] = plan
    session_id = _get_session_id(request)
    action_labels = [_action_label_for(fix_id) for fix_id in plan]
    _RUN_STATE[session_id] = {
        "queue": plan,
        "labels": action_labels,
        "results": [],
        "started_at": time.time(),
        "done": False,
    }
    return RedirectResponse("/simple/run", status_code=303)


@router.get("/run", response_class=HTMLResponse)
async def simple_run(request: Request):
    session_id = _get_session_id(request)
    state = _RUN_STATE.get(session_id)
    if not state or not state.get("queue"):
        return RedirectResponse("/simple/results", status_code=303)
    return templates.TemplateResponse(
        request,
        "simple/run.html",
        {
            "title": "Simple Mode",
            "actions": state.get("labels", []),
            "total": len(state.get("queue", [])),
        },
    )


@router.post("/api/run-next")
async def simple_run_next(request: Request):
    session_id = _get_session_id(request)
    state = _RUN_STATE.get(session_id)
    if not state:
        return JSONResponse({"done": True})

    queue = state.get("queue", [])
    results = state.get("results", [])
    index = len(results)

    if index >= len(queue):
        state["done"] = True
        return JSONResponse({"done": True})

    fix_id = queue[index]
    label = state.get("labels", [])[index] if state.get("labels") else _action_label_for(fix_id)

    try:
        result = FixEngine.run_fix(fix_id)
    except Exception as exc:
        result = {"success": False, "message": str(exc)}

    success = bool(result.get("success"))
    skipped = bool(result.get("skipped"))
    status = "skipped" if skipped else "success" if success else "failed"

    entry = {
        "label": label,
        "status": status,
        "message": result.get("message") or "",
        "details": _format_details(result),
    }
    results.append(entry)
    state["results"] = results

    done = len(results) >= len(queue)
    state["done"] = done

    return JSONResponse(
        {
            "done": done,
            "index": index,
            "status": status,
            "message": _friendly_message(status),
        }
    )


@router.get("/results", response_class=HTMLResponse)
async def simple_results(request: Request):
    session_id = _get_session_id(request)
    state = _RUN_STATE.get(session_id, {"queue": [], "results": []})
    results = state.get("results", [])
    total = len(state.get("queue", []))

    completed = [r for r in results if r.get("status") in ("success", "skipped")]
    failed = [r for r in results if r.get("status") == "failed"]

    show_pro_mode = len(failed) > 0 or total == 0

    return templates.TemplateResponse(
        request,
        "simple/results.html",
        {
            "title": "Simple Mode",
            "completed": completed,
            "failed": failed,
            "total": total,
            "show_pro_mode": show_pro_mode,
        },
    )


@router.get("/export")
async def simple_export(request: Request):
    session_id = _get_session_id(request)
    state = _RUN_STATE.get(session_id)
    if not state:
        raise HTTPException(status_code=404, detail="No results available")

    lines = [
        "DiagnOStiX Simple Mode Results",
        f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
    ]
    for entry in state.get("results", []):
        lines.append(f"- {entry.get('label', 'Action')}: {entry.get('status', 'unknown')}")
        msg = entry.get("message") or ""
        if msg:
            lines.append(f"  Note: {msg}")
        details = entry.get("details") or ""
        if details:
            lines.append("  Details:")
            for detail_line in details.splitlines():
                lines.append(f"    {detail_line}")
        lines.append("")

    content = "\n".join(lines)
    headers = {"Content-Disposition": "attachment; filename=diagnostix_simple_results.txt"}
    return PlainTextResponse(content, headers=headers)
