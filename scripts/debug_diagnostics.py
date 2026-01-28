
import sys
import os
import platform
import logging
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent.parent / "webui"))

# Configure logging
logging.basicConfig(level=logging.DEBUG)

print(f"Diagnostics Debug Tool - {platform.system()} {platform.release()}")
print("-" * 50)

try:
    print("Importing diagnostics package...")
    from diagnostics import DIAGNOSTIC_FUNCTIONS
    print("Success.")
except ImportError as e:
    print(f"Failed to import diagnostics package: {e}")
    sys.exit(1)

def run_debug(name, key):
    print(f"\nRunning {name} ({key})...")
    if key not in DIAGNOSTIC_FUNCTIONS:
        print(f"!! Function {key} not found in registry.")
        return
        
    func = DIAGNOSTIC_FUNCTIONS[key]
    try:
        result = func()
        print("--- Output Start ---")
        print(result)
        print("--- Output End ---")
    except Exception as e:
        print(f"!!! CRITICAL FAILURE in {name}: {e}")
        import traceback
        traceback.print_exc()

# 1. GPU Diagnostics
run_debug("GPU Diagnostics", "gpu_diagnostics")

# 2. Hardware Health
run_debug("Hardware Health", "hardware_health")

# 3. Disk Diagnostics
run_debug("Disk Diagnostics", "disk_diagnostics")

# 4. Check GPUtil installation explicitly
print("\nChecking GPUtil dependency...")
try:
    import GPUtil
    print(f"GPUtil imported successfully. Version: {getattr(GPUtil, '__version__', 'unknown')}")
    print(f"GPUs detected: {len(GPUtil.getGPUs())}")
except ImportError:
    print("GPUtil NOT installed.")
except Exception as e:
    print(f"GPUtil error: {e}")
