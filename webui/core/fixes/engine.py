"""
DiagnOStiX 3.0 - Fix Engine

Orchestrates fix execution with full safety checks and audit logging.
"""

import platform
import logging
import traceback
from typing import Dict, Any, Optional, List

from core.fixes.registry import FixRegistry
from core.fixes.base import FixResult, FixCategory, RiskLevel
from core.db import db_instance

logger = logging.getLogger(__name__)


class FixEngine:
    @staticmethod
    def run_fix(fix_id: str, hostname: str = None) -> Dict[str, Any]:
        """Execute a fix by ID with full safety checks and logging."""
        if hostname is None:
            hostname = platform.node()
        
        os_name = f"{platform.system()} {platform.release()}"
        fix = FixRegistry.get_fix(fix_id)
        
        if not fix:
            return {"success": False, "message": f"Fix ID '{fix_id}' not found."}

        # 1. Platform Check
        if not fix.check_platform_compatibility():
            msg = f"Fix not supported on this platform ({platform.system()})."
            db_instance.log_execution(fix_id, hostname, os_name, FixResult.SKIPPED.value, error_message=msg)
            return {"success": False, "message": msg}

        # 2. Detect (Pre-check)
        try:
            if not fix.detect():
                msg = "Condition not detected. Fix is not needed."
                db_instance.log_execution(fix_id, hostname, os_name, FixResult.SKIPPED.value, error_message=msg)
                return {"success": True, "message": msg, "skipped": True}
        except Exception as e:
            msg = f"Detection failed: {str(e)}"
            logger.error(msg)
            db_instance.log_execution(fix_id, hostname, os_name, FixResult.FAILURE.value, error_message=msg)
            return {"success": False, "message": msg}

        before_state = "Condition detected"

        # 3. Run
        try:
            result_data = fix.run()
        except Exception as e:
            error_details = traceback.format_exc()
            logger.error(f"Fix execution failed for {fix_id}: {error_details}")
            db_instance.log_execution(
                fix_id, hostname, os_name, FixResult.FAILURE.value, 
                before_state=before_state, error_message=str(e)
            )
            return {"success": False, "message": f"Execution failed: {str(e)}"}

        # 4. Verify
        try:
            is_verified = fix.verify()
            result_status = FixResult.SUCCESS.value if is_verified else FixResult.FAILURE.value
            verif_msg = "Fix verified successfully." if is_verified else "Verification failed."
            
            db_instance.log_execution(
                fix_id, hostname, os_name, result_status,
                before_state=before_state, after_state=result_data,
                error_message=None if is_verified else "Verification failed"
            )
            
            response = {"success": is_verified, "message": verif_msg, "details": result_data}
            if hasattr(fix, "requires_reboot") and fix.requires_reboot:
                response["requires_reboot"] = True
            return response
            
        except Exception as e:
            msg = f"Verification crashed: {str(e)}"
            logger.error(msg)
            db_instance.log_execution(
                fix_id, hostname, os_name, FixResult.FAILURE.value, 
                before_state=before_state, after_state=result_data, error_message=msg
            )
            return {"success": False, "message": msg}

    @staticmethod
    def get_fix_info(fix_id: str) -> Optional[Dict[str, Any]]:
        """Get metadata and detection status for a fix."""
        fix = FixRegistry.get_fix(fix_id)
        if not fix:
            return None
        
        is_needed = False
        try:
            is_needed = fix.detect()
        except:
            is_needed = False

        if hasattr(fix, "to_dict"):
            info = fix.to_dict()
            info["preview"] = fix.preview()
            info["is_needed"] = is_needed
        else:
            info = {
                "id": fix.id,
                "name": fix.name,
                "description": fix.description,
                "simple_description": getattr(fix, "simple_description", fix.description),
                "preview": fix.preview(),
                "is_needed": is_needed,
                "supported": fix.check_platform_compatibility(),
                "category": getattr(fix, "category", FixCategory.MAINTENANCE).value,
                "category_label": getattr(fix, "category", FixCategory.MAINTENANCE).label,
                "risk_level": getattr(fix, "risk_level", RiskLevel.SAFE).value,
                "risk_label": getattr(fix, "risk_level", RiskLevel.SAFE).label,
                "risk_color": getattr(fix, "risk_level", RiskLevel.SAFE).color,
                "requires_confirmation": getattr(fix, "risk_level", RiskLevel.SAFE).requires_confirmation,
                "requires_admin": getattr(fix, "requires_admin", False),
                "requires_reboot": getattr(fix, "requires_reboot", False),
                "estimated_time": getattr(fix, "estimated_time", 10),
                "tags": getattr(fix, "tags", []),
                "risk": "Safe" if getattr(fix, "is_safe", True) else "Caution"
            }
        return info

    @staticmethod
    def get_all_fix_info() -> List[Dict[str, Any]]:
        """Get metadata for all registered fixes."""
        fixes = FixRegistry.get_all_fixes()
        return [FixEngine.get_fix_info(fix.id) for fix in fixes]

    @staticmethod
    def get_fixes_by_category(category: str) -> List[Dict[str, Any]]:
        """Get all fixes in a specific category."""
        try:
            cat = FixCategory(category)
            fixes = FixRegistry.get_fixes_by_category(cat)
            return [FixEngine.get_fix_info(fix.id) for fix in fixes]
        except ValueError:
            return []

    @staticmethod
    def get_safe_fixes() -> List[Dict[str, Any]]:
        """Get all fixes that are safe to run without confirmation."""
        fixes = FixRegistry.get_safe_fixes()
        return [FixEngine.get_fix_info(fix.id) for fix in fixes]

    @staticmethod
    def run_safe_fixes(hostname: str = None) -> Dict[str, Any]:
        """Run all safe fixes that are needed."""
        results = []
        safe_fixes = FixRegistry.get_safe_fixes()
        
        for fix in safe_fixes:
            if fix.check_platform_compatibility():
                try:
                    if fix.detect():
                        result = FixEngine.run_fix(fix.id, hostname)
                        results.append({"fix_id": fix.id, "fix_name": fix.name, **result})
                except Exception as e:
                    results.append({"fix_id": fix.id, "fix_name": fix.name, "success": False, "message": str(e)})
        
        successful = sum(1 for r in results if r.get("success"))
        return {"total": len(results), "successful": successful, "failed": len(results) - successful, "results": results}
