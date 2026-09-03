"""
Integration Unit Test Suite for SportsMatrix Unified API, Settings, & Pydantic AI Chatbot
"""

import sys
import os
import pytest
from fastapi.testclient import TestClient

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

MONEYBALL_DIR = os.path.join(PROJECT_ROOT, "sportservices", "moneyball")
NETPREDICT_DIR = os.path.join(PROJECT_ROOT, "sportservices", "netpredict")
NOFREELOCKS_DIR = os.path.join(PROJECT_ROOT, "sportservices", "nofreelocks", "src")
SATURDAYSLATE_DIR = os.path.join(PROJECT_ROOT, "sportservices", "saturdayslate")

for d in [MONEYBALL_DIR, NETPREDICT_DIR, NOFREELOCKS_DIR, SATURDAYSLATE_DIR]:
    if d not in sys.path:
        sys.path.insert(0, d)

from sportsmatrix.main import app

client = TestClient(app)


def test_system_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "moneyball_mlb" in data["services"]
    assert "settings_manager" in data["services"]


def test_settings_get_and_post():
    # 1. GET Settings
    get_res = client.get("/api/v1/settings")
    assert get_res.status_code == 200
    cfg = get_res.json()
    assert "active_provider" in cfg

    # 2. POST Settings update
    cfg["active_provider"] = "openrouter"
    cfg["selected_model"] = "meta-llama/llama-3.3-70b-instruct"
    post_res = client.post("/api/v1/settings", json=cfg)
    assert post_res.status_code == 200
    updated = post_res.json()
    assert updated["active_provider"] == "openrouter"
    assert updated["selected_model"] == "meta-llama/llama-3.3-70b-instruct"


def test_fetch_available_models_openrouter():
    response = client.get("/api/v1/settings/models?provider=openrouter")
    assert response.status_code == 200
    data = response.json()
    assert data["provider"] == "openrouter"
    assert "models" in data
    assert len(data["models"]) > 0


def test_fetch_available_models_ollama():
    # Local Ollama
    res_local = client.get("/api/v1/settings/models?provider=ollama_local")
    assert res_local.status_code == 200
    data_local = res_local.json()
    assert data_local["provider"] == "ollama_local"
    assert "models" in data_local

    # Ollama Cloud
    res_cloud = client.get("/api/v1/settings/models?provider=ollama_cloud")
    assert res_cloud.status_code == 200
    data_cloud = res_cloud.json()
    assert data_cloud["provider"] == "ollama_cloud"
    assert "models" in data_cloud


def test_chatbot_endpoint():
    payload = {"prompt": "Who is projected to win the Chiefs vs 49ers NFL matchup?"}
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert len(data["response"]) > 0


def test_mlb_predict_endpoint():
    response = client.get("/api/v1/mlb/predict")
    assert response.status_code == 200
    data = response.json()
    assert "predictions" in data


def test_basketball_predict_endpoint():
    response = client.get("/api/v1/basketball/nba/predictions?date=2026-09-02")
    assert response.status_code == 200
    data = response.json()
    assert data["league"] == "NBA"


def test_nfl_predict_endpoint():
    payload = {
        "home_team": "KC",
        "away_team": "SF",
        "vegas_spread": -2.5,
        "vegas_total": 47.5,
        "include_explanation": True
    }
    response = client.post("/api/v1/nfl/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["home_team"] == "KC"


def test_cfb_ratings_endpoint():
    response = client.get("/api/v1/cfb/ratings?season=2025")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
