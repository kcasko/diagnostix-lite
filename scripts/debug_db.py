import sys
import logging
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent.parent / "webui"))

from core.db import db_instance

logging.basicConfig(level=logging.DEBUG)

def debug_db():
    print(f"DB Path calculated: {db_instance.db_path}")
    
    print("Connecting...")
    try:
        db_instance.connect()
        print("Connected.")
    except Exception as e:
        print(f"Connect failed: {e}")
        return

    print("Attempting to log execution...")
    try:
        db_instance.log_execution(
            fix_id="debug_test",
            hostname="debug-host",
            os_name="TestOS",
            result="success",
            condition_id="manual",
            before_state="test_before",
            after_state="test_after",
            error_message=None
        )
        print("Log execution called.")
    except Exception as e:
        print(f"Log execution crashed: {e}")

    print("Reading history...")
    history = db_instance.get_history()
    print(f"History entries: {len(history)}")
    for entry in history:
        print(f" - {entry['timestamp']} | {entry['fix_id']} | {entry['result']}")

if __name__ == "__main__":
    debug_db()
