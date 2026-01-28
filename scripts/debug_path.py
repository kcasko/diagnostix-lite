
import subprocess
import os
from pathlib import Path

# Path to a script we know exists (one of the scripts failing)
script_path = Path(r"e:\Repos\diagnostix\scripts\quick_repair.sh")

print(f"Original Windows Path: {script_path}")
print(f"Exists? {script_path.exists()}")

if script_path.exists():
    # 1. Test as_posix()
    posix_path = script_path.as_posix()
    print(f"\nTesting POSIX Path: {posix_path}")
    try:
        res = subprocess.run(["bash", posix_path], capture_output=True, text=True)
        print(f"Return Code: {res.returncode}")
        print(f"Stdout: {res.stdout.strip()}")
        print(f"Stderr: {res.stderr.strip()}")
    except Exception as e:
        print(f"Error: {e}")

    # 2. Test str() (the old broken way, just to confirm it reproduces the error)
    str_path = str(script_path)
    print(f"\nTesting str() Path: {str_path}")
    try:
        res = subprocess.run(["bash", str_path], capture_output=True, text=True)
        print(f"Return Code: {res.returncode}")
        print(f"Stdout: {res.stdout.strip()}")
        print(f"Stderr: {res.stderr.strip()}")
    except Exception as e:
        print(f"Error: {e}")

    # 3. Test relative path (if we are in root)
    rel_path = "scripts/quick_repair.sh"
    print(f"\nTesting Relative Path: {rel_path}")
    try:
        res = subprocess.run(["bash", rel_path], capture_output=True, text=True)
        print(f"Return Code: {res.returncode}")
        print(f"Stdout: {res.stdout.strip()}")
        print(f"Stderr: {res.stderr.strip()}")
    except Exception as e:
        print(f"Error: {e}")
else:
    print("Script file not found at expected location!")
