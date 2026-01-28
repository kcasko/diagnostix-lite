import sys
import os
import logging
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent.parent / "webui"))

from core.db import db_instance
from core.fixes.registry import FixRegistry
from core.fixes.engine import FixEngine
import core.fixes.implementations.general
import core.fixes.implementations.network
import core.fixes.implementations.process

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("verifier")

def test_fix_engine():
    print("=== DiagnOStiX Fix Engine Verification ===")
    
    # 1. Initialize DB
    print("\n[1] Initializing Database...")
    try:
        db_instance.connect()
        print("Success: Database connected.")
    except Exception as e:
        print(f"FAILED: {e}")
        return

    # 2. Check Registry
    print("\n[2] Checking Registry...")
    fixes = FixRegistry.get_all_fixes()
    print(f"Found {len(fixes)} registered fixes.")
    for f in fixes:
        print(f" - {f.id}: {f.name} (Safe: {f.is_safe}, Platform: {f.supported_platforms})")
    
    if len(fixes) < 5:
        print("FAILED: Expected at least 5 fixes.")
        return
    else:
        print("Success: Registry populated.")

    # 3. Test Detection (Dry Run)
    print("\n[3] Testing Detection (Dry Run)...")
    for f in fixes:
        try:
            compatible = f.check_platform_compatibility()
            needed = f.detect() if compatible else "N/A"
            print(f" - {f.id}: Compatible={compatible}, Detect={needed}")
        except Exception as e:
            print(f" - {f.id}: Error during detect - {e}")

    # 4. Test Execution & Audit Log (Mock or Safe Fix)
    print("\n[4] Testing Execution & Logging (running 'flush_dns')...")
    # Flush DNS is generally safe to run repeatedly
    result = FixEngine.run_fix("flush_dns")
    print(f"Result: {result}")
    
    if not result["success"]:
        print("WARNING: Flush DNS failed (this might differ by OS/Permission).")
    
    # Check DB
    print("\n[5] Verifying Audit Log in DB...")
    history = db_instance.get_history(limit=1)
    if history:
        last = history[0]
        print(f"Log Found: ID={last['id']}, Fix={last['fix_id']}, Result={last['result']}")
        if last['fix_id'] == "flush_dns":
             print("Success: Audit log verified.")
        else:
             print("FAILED: Last log entry does not match.")
    else:
        print("FAILED: No history found.")

if __name__ == "__main__":
    test_fix_engine()
