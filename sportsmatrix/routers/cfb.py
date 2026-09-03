"""
FastAPI Router for SaturdaySlate College Football (CFB) Engine (/api/v1/cfb)
"""

import sys
import os
from typing import Optional, List
from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SATURDAYSLATE_DIR = os.path.join(PROJECT_ROOT, "sportservices", "saturdayslate")
if SATURDAYSLATE_DIR not in sys.path:
    sys.path.insert(0, SATURDAYSLATE_DIR)

from src.api.server import (
    get_games, get_team_ratings, predict_week, get_edge_report, run_custom_simulation, run_backtest,
    GameResponse, TeamRatingResponse, GamePredictionOutput, PredictRequest, SimulationRequest, SimulationResponse, BacktestRequest, BacktestResponse,
    get_db, db_mgr
)
from src.data.ingestion import DataIngestionPipeline

router = APIRouter(prefix="/api/v1/cfb", tags=["College Football (SaturdaySlate)"])


@router.get("/games", response_model=List[GameResponse])
def get_cfb_games(
    season: Optional[int] = Query(None, description="Filter by season"),
    week: Optional[int] = Query(None, description="Filter by week"),
    team: Optional[str] = Query(None, description="Filter by team name"),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    session: Session = Depends(get_db)
):
    """Fetches stored College Football games matching filter criteria."""
    return get_games(season=season, week=week, team=team, completed=completed, session=session)


@router.get("/ratings", response_model=List[TeamRatingResponse])
def get_cfb_team_ratings(
    season: int = Query(2025, description="Target season"),
    session: Session = Depends(get_db)
):
    """Fetches dynamic Elo and Glicko-2 ratings for all College Football teams."""
    try:
        return get_team_ratings(season=season, session=session)
    except HTTPException as e:
        if e.status_code == 404:
            # Auto-seed synthetic data for requested season if DB is unpopulated
            ingest = DataIngestionPipeline(db_mgr)
            ingest.sync_season_data(year=season, weeks=[1, 2, 3, 4, 5])
            return get_team_ratings(season=season, session=session)
        raise e


@router.post("/predict", response_model=List[GamePredictionOutput])
def predict_cfb_week(req: PredictRequest):
    """Executes pre-kickoff prediction and Monte Carlo simulation for CFB target week."""
    return predict_week(req)


@router.get("/edge-report")
def get_cfb_edge_report(
    season: int = Query(2025),
    week: int = Query(13),
    team: Optional[str] = Query(None),
    format: str = Query("json", enum=["json", "table", "markdown", "csv"])
):
    """Fetches formatted Line Edge Report for College Football games."""
    return get_edge_report(season=season, week=week, team=team, format=format)


@router.post("/simulate", response_model=SimulationResponse)
def simulate_cfb_matchup(req: SimulationRequest):
    """Runs Monte Carlo simulation for a custom CFB matchup parameter set."""
    return run_custom_simulation(req)


@router.post("/backtest", response_model=BacktestResponse)
def backtest_cfb_seasons(req: BacktestRequest):
    """Runs out-of-sample walk-forward backtest across College Football seasons."""
    return run_backtest(req)
