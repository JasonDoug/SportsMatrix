"""
Integration Unit Test Suite for SportsMatrix Unified API & Pydantic AI Chatbot
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
    assert "pydantic_ai_chatbot" in data["services"]


def test_chatbot_endpoint():
    payload = {"prompt": "Who is projected to win the Chiefs vs 49ers NFL matchup?"}
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert len(data["response"]) > 0
    assert "NoFreeLocks (NFL)" in data["service_sources"]


def test_mlb_predict_endpoint():
    response = client.get("/api/v1/mlb/predict?date=2025-08-30")
    assert response.status_code == 200
    data = response.json()
    assert "predictions" in data
    assert "total_games" in data


def test_basketball_predict_endpoint():
    response = client.get("/api/v1/basketball/nba/predictions?date=2026-09-02")
    assert response.status_code == 200
    data = response.json()
    assert data["league"] == "NBA"
    assert "predictions" in data


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
    assert "win_probability_home" in data
    assert "explanation" in data


def test_cfb_ratings_endpoint():
    response = client.get("/api/v1/cfb/ratings?season=2025")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "elo_rating" in data[0]
