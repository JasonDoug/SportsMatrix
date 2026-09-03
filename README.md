# SportsMatrix 🏆

**SportsMatrix** is a unified sports prediction and analytics platform integrating specialized machine learning, Monte Carlo simulation, statistical modeling engines, and a **Pydantic AI Chatbot Agent** across multiple professional and collegiate sports.

## 📦 Architecture & Sport Services

SportsMatrix organizes its underlying engine components using Git submodules located under `sportservices/`:

| Service | Sport / League | Capabilities & Highlights | Submodule Repository |
| :--- | :--- | :--- | :--- |
| **Moneyball** | MLB Baseball | Live slate predictions, Statcast pitch analytics, Monte Carlo matchup simulations, and market ROI backtesting. | [JasonDoug/Moneyball](https://github.com/JasonDoug/Moneyball) |
| **NetPredict** | Basketball (NBA, WNBA, NCAAM, NCAAW) | Four-factor basketball prediction engine integrated with live consensus betting lines. | [JasonDoug/NetPredict](https://github.com/JasonDoug/NetPredict) |
| **NoFreeLocks** | NFL Football | Tabular ML ensemble (XGBoost, LightGBM, CatBoost, Elo) with narrative rationale generation and injury news extraction. | [JasonDoug/NoFreeLocks](https://github.com/JasonDoug/NoFreeLocks) |
| **SaturdaySlate** | College Football (CFB) | Dynamic Elo/Glicko team ratings, pre-kickoff line edge reports, and out-of-sample walk-forward backtesters. | [JasonDoug/SaturdaySlate](https://github.com/JasonDoug/SaturdaySlate) |

---

## 🤖 Pydantic AI Chatbot & Multi-Provider LLM Engine

SportsMatrix features a single top-level **Pydantic AI LLM Assistant** (`sportsmatrix.chatbot.agent`) equipped with tool functions to query all underlying sport services.

### Supported Providers & Models

Set up and switch between any LLM provider directly in the Web UI Settings tab (`⚙️ LLM Provider Settings`) or via API:

- 🌐 **OpenRouter**: Route queries through 100+ cloud models (e.g. `meta-llama/llama-3.3-70b-instruct`, `anthropic/claude-3.5-sonnet`, `deepseek/deepseek-r1`, `openai/gpt-4o`).
- 🦙 **Local Ollama**: Connect to your local Ollama daemon at `http://localhost:11434` (e.g. `qwen2.5:7b`, `llama3.1:8b`).
- ☁️ **Ollama Cloud**: Query remote Ollama host endpoints (`https://ollama.com`).
- ⚡ **Direct APIs**: OpenAI (`gpt-4o`), Google Gemini (`gemini-2.0-flash`), Anthropic (`claude-3-5-sonnet-latest`).
- 🧪 **Mock / Test Mode**: Offline test mode with smart tool-execution dispatcher.

---

## 🚀 How to Start the Suite

### 1. Clone & Setup

```bash
# Clone SportsMatrix with submodules
git clone --recurse-submodules https://github.com/JasonDoug/SportsMatrix.git
cd SportsMatrix

# Create virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Launch the Server

Run the launcher script to start the unified FastAPI gateway, sports engines, and Pydantic AI chatbot:

```bash
python run_sportsmatrix.py
```

Open **[http://localhost:8000](http://localhost:8000)** in your browser:
- 🤖 **Pydantic AI Chatbot UI**: Ask natural language questions.
- ⚙️ **Settings Tab**: Configure provider API keys and dynamically discover/select working models.
- ⚾ **MLB / 🏀 Basketball / 🏈 NFL / 🏈 CFB Tabs**: Inspect live engine outputs.
- 📄 **OpenAPI Docs**: Navigate to [http://localhost:8000/docs](http://localhost:8000/docs).

---

## 💡 Example Queries & API Usage

### 1. 🤖 Pydantic AI Chatbot (`POST /api/v1/chat`)

Send natural language queries to the top-level LLM agent:

```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Who is projected to win the Chiefs vs 49ers NFL matchup?"}'
```

**Example Natural Language Prompts**:
- 🏈 **NFL Matchups**: *"Predict the outcome for SF @ KC with spread edge and win probabilities."*
- 🏈 **NFL Roster News**: *"Extract injury status: Patrick Mahomes trained fully, Deebo Samuel is questionable with a hamstring tweak."*
- ⚾ **MLB Slate**: *"Show me the Moneyball MLB predictions and daily locks for today's slate."*
- ⚾ **MLB Monte Carlo Sim**: *"Run 10,000 Monte Carlo simulations for San Francisco Giants vs Los Angeles Dodgers."*
- 🏀 **NBA Basketball**: *"What are the NetPredict predictions and four-factor ratings for upcoming NBA games?"*
- 🏀 **College Hoops**: *"Show me the predictions for NCAAM basketball games."*
- 🏈 **CFB Ratings**: *"Show me the top 10 College Football team Elo ratings from SaturdaySlate."*
- 🏈 **CFB Line Edge**: *"Get the week 13 College Football edge report."*

---

### 2. ⚾ Moneyball MLB Engine (`/api/v1/mlb`)

- **Slate Predictions**:
  ```bash
  curl "http://localhost:8000/api/v1/mlb/predict?date=2025-08-30&model_type=xgboost"
  ```
- **Monte Carlo Simulation**:
  ```bash
  curl -X POST "http://localhost:8000/api/v1/mlb/simulate" \
    -H "Content-Type: application/json" \
    -d '{"home_team": "LAD", "away_team": "SF", "num_simulations": 10000, "k_line": 6.5}'
  ```

---

### 3. 🏀 NetPredict Basketball Engine (`/api/v1/basketball`)

- **NBA Predictions**:
  ```bash
  curl "http://localhost:8000/api/v1/basketball/nba/predictions?date=2026-09-02"
  ```
- **WNBA / NCAAM / NCAAW Predictions**:
  ```bash
  curl "http://localhost:8000/api/v1/basketball/ncaam/predictions?date=2026-09-02"
  ```

---

### 4. 🏈 NoFreeLocks NFL Engine (`/api/v1/nfl`)

- **Game Matchup Prediction**:
  ```bash
  curl -X POST "http://localhost:8000/api/v1/nfl/predict" \
    -H "Content-Type: application/json" \
    -d '{"home_team": "KC", "away_team": "SF", "vegas_spread": -2.5, "vegas_total": 47.5}'
  ```
- **Player News Extraction**:
  ```bash
  curl -X POST "http://localhost:8000/api/v1/nfl/extract-news" \
    -H "Content-Type: application/json" \
    -d '{"text": "Patrick Mahomes trained fully. Deebo Samuel is questionable."}'
  ```

---

### 5. 🏈 SaturdaySlate College Football Engine (`/api/v1/cfb`)

- **Team Ratings**:
  ```bash
  curl "http://localhost:8000/api/v1/cfb/ratings?season=2025"
  ```
- **Pre-Kickoff Line Edge Report**:
  ```bash
  curl "http://localhost:8000/api/v1/cfb/edge-report?season=2025&week=13&format=json"
  ```

---

### 6. ⚙️ Settings & Dynamic Model Discovery (`/api/v1/settings`)

- **Fetch Available Models for OpenRouter**:
  ```bash
  curl "http://localhost:8000/api/v1/settings/models?provider=openrouter"
  ```
- **Fetch Available Local Ollama Models**:
  ```bash
  curl "http://localhost:8000/api/v1/settings/models?provider=ollama_local&ollama_local_base_url=http://localhost:11434"
  ```
- **Update Active Provider & Model**:
  ```bash
  curl -X POST "http://localhost:8000/api/v1/settings" \
    -H "Content-Type: application/json" \
    -d '{
      "active_provider": "openrouter",
      "selected_model": "meta-llama/llama-3.3-70b-instruct",
      "openrouter_api_key": "sk-or-v1-your-key-here"
    }'
  ```

---

## 🧪 Running Unit Tests

Execute the automated test suite covering all 4 engines, settings discovery, and Pydantic AI chatbot:

```bash
pytest tests/test_sportsmatrix_api.py -v
```

---

## 📄 License

Apache License 2.0
