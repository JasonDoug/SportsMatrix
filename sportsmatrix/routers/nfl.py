"""
FastAPI Router for NoFreeLocks NFL Prediction Service (/api/v1/nfl)
"""

import sys
import os
from fastapi import APIRouter, HTTPException

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
NOFREELOCKS_DIR = os.path.join(PROJECT_ROOT, "sportservices", "nofreelocks", "src")
if NOFREELOCKS_DIR not in sys.path:
    sys.path.insert(0, NOFREELOCKS_DIR)

from nofreelocks.api.server import (
    predict_game, evaluate_pipeline, extract_news_status,
    GamePredictionRequest, EvaluationRequest, NewsExtractionRequest,
    ensemble_predictor
)

router = APIRouter(prefix="/api/v1/nfl", tags=["NFL (NoFreeLocks)"])


@router.post("/predict")
def predict_nfl_matchup(req: GamePredictionRequest):
    """Predicts NFL game outcome, win probability, point margin, total, and optional LLM narrative explanation."""
    # Ensure model initialization
    if ensemble_predictor is None or not ensemble_predictor.is_fitted:
        from nofreelocks.data import generate_synthetic_nfl_data, preprocess_nfl_games
        from nofreelocks.features import FeaturePipeline
        from nofreelocks.models import EnsembleNFLPredictor
        pipe = FeaturePipeline()
        df_boot = generate_synthetic_nfl_data(seasons=[2022, 2023, 2024], seed=42)
        df_clean = preprocess_nfl_games(df_boot)
        df_feat = pipe.transform(df_clean)
        X, y_win, y_spread, y_total = pipe.get_features_and_targets(df_feat)
        ens = EnsembleNFLPredictor()
        ens.fit_ensemble(df_clean, X, y_win, y_spread, y_total)
        import nofreelocks.api.server as nfl_module
        nfl_module.ensemble_predictor = ens

    return predict_game(req)


@router.post("/evaluate")
def evaluate_nfl_walk_forward(req: EvaluationRequest):
    """Runs expanding walk-forward time-series validation across NFL historical seasons."""
    return evaluate_pipeline(req)


@router.post("/extract-news")
def extract_nfl_roster_news(req: NewsExtractionRequest):
    """Extracts player injury status and roster news updates from raw text."""
    return extract_news_status(req)
