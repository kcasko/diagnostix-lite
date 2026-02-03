
import os
import sys
import threading
import webbrowser
import uvicorn
import time
from main import app

def open_browser():
    """Wait for server to start then open browser."""
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    try:
        # Set thread to open browser
        threading.Thread(target=open_browser, daemon=True).start()
        
        # Run server (blocking)
        # Use 127.0.0.1 explicitly for security in the desktop app context
        print("Starting DiagnOStiX Desktop App...")
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("\nCRITICAL ERROR: The application failed to start.")
        print(f"Error details: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)
