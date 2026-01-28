import platform
import logging
import traceback
from typing import Dict, Any, Optional

from .registry import FixRegistry
from .base import FixResult
from ..db import db_instance

logger = logging.getLogger(__name__)

class FixEngine:
    @staticmethod
    def run_fix(fix_id: str, hostname: str = None) -> Dict[str, Any]:
        """
        Execute a fix by ID with full safety checks and logging.
        """
        if hostname is None:
            hostname = platform.node()
        
        os_name = f"{platform.system()} {platform.release()}"
        fix = FixRegistry.get_fix(fix_id)
        
        if not fix:
            return {
                "success": False,
                "message": f"Fix ID '{fix_id}' not found."
            }

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

        # Capture Before State (Snapshot - simplified for now)
        before_state = "Condition detected"

        # 3. Run
        try:
            result_data = fix.run()
        except Exception as e:
            error_details = traceback.format_exc()
            logger.error(f"Fix execution failed for {fix_id}: {error_details}")
            db_instance.log_execution(
                fix_id, hostname, os_name, FixResult.FAILURE.value, 
                before_state=before_state,
                error_message=str(e)
            )
            return {"success": False, "message": f"Execution failed: {str(e)}"}

        # 4. Verify
        try:
            is_verified = fix.verify()
            result_status = FixResult.SUCCESS.value if is_verified else FixResult.FAILURE.value
            verif_msg = "Fix verified successfully." if is_verified else "Verification failed after execution."
            
            db_instance.log_execution(
                fix_id, hostname, os_name, result_status,
                before_state=before_state,
                after_state=result_data,
                error_message=None if is_verified else "Verification failed"
            )
            
            return {
                "success": is_verified, 
                "message": verif_msg, 
                "details": result_data
            }
            
        except Exception as e:
            msg = f"Verification process crashed: {str(e)}"
            logger.error(msg)
            db_instance.log_execution(
                fix_id, hostname, os_name, FixResult.FAILURE.value, 
                before_state=before_state,
                after_state=result_data,
                error_message=msg
            )
            return {"success": False, "message": msg}

    @staticmethod
    def get_fix_info(fix_id: str) -> Dict[str, Any]:
        """Get metadata and detection status for a fix."""
        fix = FixRegistry.get_fix(fix_id)
        if not fix:
            return None
        
        is_needed = False
        try:
            is_needed = fix.detect()
        except:
            is_needed = False # If detection fails, assume false or handle error? Safe default.

        return {
            "id": fix.id,
            "name": fix.name,
            "description": fix.description,
            "preview": fix.preview(),
            "is_needed": is_needed,
            "supported": fix.check_platform_compatibility(),
            "risk": "Safe" if fix.is_safe else "Caution"
        }
