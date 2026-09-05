"""
Launcher script to run the FastAPI Backend server.
"""

import sys
from pathlib import Path
import uvicorn

# Add backend directory to sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

if __name__ == "__main__":
    print("========================================================================")
    print("    Starting Explainable AI Diabetic Retinopathy FastAPI Server         ")
    print("    URL: http://127.0.0.1:8000                                          ")
    print("    API Documentation: http://127.0.0.1:8000/docs                       ")
    print("========================================================================")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
