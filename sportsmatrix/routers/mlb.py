"""
FastAPI Router for Moneyball MLB Prediction Engine (/api/v1/mlb)
"""

import sys
import os
import json
from typing import Optional
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MONEYBALL_DIR = os.path.join(PROJECT_ROOT, "sportservices", "moneyball")
if MONEYBALL_DIR not in sys.path:
    sys.path.insert(0, MONEYBALL_DIR)

from mlb_engine.server import get_slate_predictions, run_simulation, run_backtest, SimulationRequest, BacktestRequest

router = APIRouter(prefix="/api/v1/mlb", tags=["MLB (Moneyball)"])


@router.get("/predict")
def predict_mlb_slate(
    date: Optional[str] = Query(None, description="Date YYYY-MM-DD"),
    season: int = Query(2025),
    model_type: str = Query("xgboost"),
    pitcher_rolling: bool = Query(True),
    statcast: bool = Query(True),
    platoon: bool = Query(True),
    pitch_matchups: bool = Query(True),
    bullpen: bool = Query(True),
    weather_park: bool = Query(True),
    travel_rest: bool = Query(True),
    min_ev: float = Query(0.02),
    kelly_fraction: float = Query(0.25),
    offline: bool = Query(False)
):
    """Fetches Moneyball live slate predictions, expected scores, win probabilities, and daily locks for MLB."""
    resp = get_slate_predictions(
        date=date, season=season, model_type=model_type,
        pitcher_rolling=pitcher_rolling, statcast=statcast, platoon=platoon,
        pitch_matchups=pitch_matchups, bullpen=bullpen, weather_park=weather_park,
        travel_rest=travel_rest, min_ev=min_ev, kelly_fraction=kelly_fraction, offline=offline
    )
    return json.loads(resp.body.decode("utf-8"))


@router.post("/simulate")
def simulate_mlb_matchup(req: SimulationRequest):
    """Runs Monte Carlo simulation for a target MLB matchup."""
    resp = run_simulation(req)
    return json.loads(resp.body.decode("utf-8"))


@router.post("/backtest")
def backtest_mlb_season(req: BacktestRequest):
    """Executes seasonal market ROI backtest for MLB betting strategies."""
    resp = run_backtest(req)
    return json.loads(resp.body.decode("utf-8"))
