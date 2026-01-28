#!/bin/bash
echo "Starting DiagnOStiX WebUI..."
echo
cd webui
echo "Activating virtual environment..."
source venv/Scripts/activate
echo
echo "Starting FastAPI server on http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo
uvicorn main:app --reload --host 0.0.0.0 --port 8000
