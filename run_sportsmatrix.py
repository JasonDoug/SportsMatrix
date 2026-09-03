#!/usr/bin/env python3
"""
SportsMatrix Server Launcher
Runs the unified SportsMatrix FastAPI service and Pydantic AI chatbot backend using Uvicorn.
"""

import sys
import os
import uvicorn

# Ensure repository root and submodule paths are in sys.path
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

MONEYBALL_DIR = os.path.join(PROJECT_ROOT, "sportservices", "moneyball")
NETPREDICT_DIR = os.path.join(PROJECT_ROOT, "sportservices", "netpredict")
NOFREELOCKS_DIR = os.path.join(PROJECT_ROOT, "sportservices", "nofreelocks", "src")
SATURDAYSLATE_DIR = os.path.join(PROJECT_ROOT, "sportservices", "saturdayslate")

for d in [MONEYBALL_DIR, NETPREDICT_DIR, NOFREELOCKS_DIR, SATURDAYSLATE_DIR]:
    if d not in sys.path:
        sys.path.insert(0, d)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Starting SportsMatrix Unified API & Pydantic AI Chatbot on http://localhost:{port}")
    uvicorn.run("sportsmatrix.main:app", host="0.0.0.0", port=port, reload=True)
