# SportsMatrix 🏆

**SportsMatrix** is a unified sports prediction and analytics platform integrating specialized machine learning, Monte Carlo simulation, and statistical modeling engines across multiple professional and collegiate sports.

It features a **Unified FastAPI Service** and a **Pydantic AI Chatbot LLM Agent** that can query all underlying sport services via tool calls.

---

## 📦 Architecture & Integrated Sport Engines

SportsMatrix organizes its underlying engines as Git submodules located under `sportservices/`:

| Module | Sport / League | Description | Repository |
| :--- | :--- | :--- | :--- |
| **Moneyball** (`sportservices/moneyball`) | MLB Baseball | Live slate predictions, Monte Carlo matchup simulations, Statcast pitch analytics, and market ROI backtester. | [JasonDoug/Moneyball](https://github.com/JasonDoug/Moneyball) |
| **NetPredict** (`sportservices/netpredict`) | Basketball (NBA, WNBA, NCAAM, NCAAW) | Four-factor basketball prediction engine integrated with live consensus betting lines. | [JasonDoug/NetPredict](https://github.com/JasonDoug/NetPredict) |
| **NoFreeLocks** (`sportservices/nofreelocks`) | NFL Football | Tabular ML ensemble (XGBoost, LightGBM, CatBoost, Elo) with LLM narrative rationale and injury news extraction. | [JasonDoug/NoFreeLocks](https://github.com/JasonDoug/NoFreeLocks) |
| **SaturdaySlate** (`sportservices/saturdayslate`) | College Football (CFB) | Dynamic Elo/Glicko ratings, pre-kickoff edge detection reports, and out-of-sample backtesters. | [JasonDoug/SaturdaySlate](https://github.com/JasonDoug/SaturdaySlate) |

---

## 🤖 Pydantic AI Chatbot Agent

SportsMatrix includes a **Pydantic AI LLM Agent** (`sportsmatrix.chatbot.agent`) equipped with tools for querying all 4 sport services:

- `tool_predict_mlb_slate` (MLB predictions)
- `tool_simulate_mlb_matchup` (MLB Monte Carlo simulation)
- `tool_predict_basketball` (NBA / WNBA / NCAAM / NCAAW predictions)
- `tool_predict_nfl_game` (NFL game margin, total, win probability, & LLM rationale)
- `tool_extract_nfl_news` (NFL player injury / news extraction)
- `tool_predict_cfb_slate` (College Football week predictions)
- `tool_get_cfb_ratings` (College Football Elo & Glicko ratings)

Users can send natural language prompts to `POST /api/v1/chat`:

```json
POST /api/v1/chat
{
  "prompt": "Who is projected to win the Chiefs vs 49ers NFL matchup?"
}
```

---

## 🌐 Unified API Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `GET /` | `GET` | Interactive SportsMatrix Portal & Chatbot Web UI |
| `GET /health` | `GET` | System health check across all 4 sport engines |
| `POST /api/v1/chat` | `POST` | Pydantic AI Chatbot query endpoint |
| `GET /api/v1/mlb/predict` | `GET` | MLB daily slate predictions & locks |
| `POST /api/v1/mlb/simulate` | `POST` | MLB Monte Carlo matchup simulator |
| `POST /api/v1/mlb/backtest` | `POST` | MLB market ROI backtest |
| `GET /api/v1/basketball/{league}/predictions` | `GET` | Basketball game predictions (nba, wnba, ncaam, ncaaw) |
| `POST /api/v1/nfl/predict` | `POST` | NFL game prediction & narrative explanation |
| `POST /api/v1/nfl/extract-news` | `POST` | NFL player roster / injury news parser |
| `GET /api/v1/cfb/ratings` | `GET` | College Football team Elo & Glicko ratings |
| `GET /api/v1/cfb/edge-report` | `GET` | CFB pre-kickoff line edge report |

---

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone --recurse-submodules https://github.com/JasonDoug/SportsMatrix.git
cd SportsMatrix

# Create virtual environment & install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the Unified Server

```bash
python run_sportsmatrix.py
```

Open [http://localhost:8000](http://localhost:8000) in your browser to access the Interactive Portal, Chatbot UI, and OpenAPI docs (`/docs`).

### 3. Run Tests

```bash
pytest tests/test_sportsmatrix_api.py -v
```

---

## 📄 License

Apache License 2.0
