"""
FastAPI Router for NetPredict Basketball Service (/api/v1/basketball)
Supports NBA, WNBA, NCAAM, and NCAAW.
"""

import sys
import os
from fastapi import APIRouter, Query, HTTPException

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
NETPREDICT_DIR = os.path.join(PROJECT_ROOT, "sportservices", "netpredict")
if NETPREDICT_DIR not in sys.path:
    sys.path.insert(0, NETPREDICT_DIR)

from backend.app.main import get_league_predictions, health_check as netpredict_health

router = APIRouter(prefix="/api/v1/basketball", tags=["Basketball (NetPredict)"])


@router.get("/health")
def get_health():
    """Checks NetPredict engine health and Odds API key status."""
    return netpredict_health()


@router.get("/{league}/predictions")
def predict_league_games(
    league: str,
    date: str = Query("2026-09-02", description="Date YYYY-MM-DD")
):
    """Fetches basketball game predictions and four-factor ratings for NBA, WNBA, NCAAM, or NCAAW."""
    return get_league_predictions(league=league, date=date)
