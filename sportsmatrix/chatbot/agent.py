"""
SportsMatrix Pydantic AI Chatbot LLM Agent
Supports OpenRouter, Local Ollama, Ollama Cloud, OpenAI, Gemini, Anthropic, and Mock/Test providers.
Registers tool functions for querying Moneyball (MLB), NetPredict (Basketball),
NoFreeLocks (NFL), and SaturdaySlate (CFB).
"""

import sys
import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

# Path setup for subservices
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MONEYBALL_DIR = os.path.join(PROJECT_ROOT, "sportservices", "moneyball")
NETPREDICT_DIR = os.path.join(PROJECT_ROOT, "sportservices", "netpredict")
NOFREELOCKS_DIR = os.path.join(PROJECT_ROOT, "sportservices", "nofreelocks", "src")
SATURDAYSLATE_DIR = os.path.join(PROJECT_ROOT, "sportservices", "saturdayslate")

for d in [MONEYBALL_DIR, NETPREDICT_DIR, NOFREELOCKS_DIR, SATURDAYSLATE_DIR]:
    if d not in sys.path:
        sys.path.insert(0, d)

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from sportsmatrix.chatbot.schemas import ChatRequest, ChatResponse, ToolCallLog
from sportsmatrix.chatbot.settings import SettingsConfig, load_settings

logger = logging.getLogger(__name__)

# --- TOOL IMPLEMENTATIONS ---

def tool_predict_mlb_slate(date: Optional[str] = None, model_type: str = "xgboost") -> Dict[str, Any]:
    """Fetches daily slate predictions and win probabilities for MLB games (Moneyball Engine). Defaults to dynamic current date."""
    target_date = date if date else datetime.now().strftime("%Y-%m-%d")
    try:
        from mlb_engine.server import get_slate_predictions
        resp = get_slate_predictions(date=target_date, model_type=model_type)
        return json.loads(resp.body.decode("utf-8"))
    except Exception as e:
        logger.error(f"Error calling MLB predict: {e}")
        return {"error": str(e), "service": "Moneyball MLB"}


def tool_simulate_mlb_matchup(home_team: str = "LAD", away_team: str = "SF", num_simulations: int = 10000) -> Dict[str, Any]:
    """Runs a Monte Carlo game simulation for an MLB matchup (Moneyball Engine)."""
    try:
        from mlb_engine.server import run_simulation, SimulationRequest
        req = SimulationRequest(home_team=home_team, away_team=away_team, num_simulations=num_simulations)
        resp = run_simulation(req)
        return json.loads(resp.body.decode("utf-8"))
    except Exception as e:
        logger.error(f"Error calling MLB simulate: {e}")
        return {"error": str(e), "service": "Moneyball MLB"}


def tool_predict_basketball(league: str = "nba", date: Optional[str] = None) -> Dict[str, Any]:
    """Fetches basketball game predictions for NBA, WNBA, NCAAM, or NCAAW (NetPredict Engine). Defaults to dynamic current date."""
    target_date = date if date else datetime.now().strftime("%Y-%m-%d")
    try:
        from backend.app.main import get_league_predictions
        return get_league_predictions(league=league, date=target_date)
    except Exception as e:
        logger.error(f"Error calling Basketball predict: {e}")
        return {"error": str(e), "service": "NetPredict Basketball"}


def tool_predict_nfl_game(
    home_team: str = "KC",
    away_team: str = "SF",
    vegas_spread: float = -2.5,
    vegas_total: float = 47.5,
    include_explanation: bool = True
) -> Dict[str, Any]:
    """Predicts NFL game outcome, point margin, total, and LLM explanation (NoFreeLocks Engine)."""
    try:
        from nofreelocks.api.server import predict_game, GamePredictionRequest, ensemble_predictor
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
        
        req = GamePredictionRequest(
            home_team=home_team,
            away_team=away_team,
            vegas_spread=vegas_spread,
            vegas_total=vegas_total,
            include_explanation=include_explanation
        )
        return predict_game(req)
    except Exception as e:
        logger.error(f"Error calling NFL predict: {e}")
        return {"error": str(e), "service": "NoFreeLocks NFL"}


def tool_extract_nfl_news(text: str) -> Dict[str, Any]:
    """Extracts NFL player injury and roster news using NLP (NoFreeLocks Engine)."""
    try:
        from nofreelocks.api.server import extract_news_status, NewsExtractionRequest
        req = NewsExtractionRequest(text=text)
        return extract_news_status(req)
    except Exception as e:
        logger.error(f"Error calling NFL news extraction: {e}")
        return {"error": str(e), "service": "NoFreeLocks NFL"}


def tool_predict_cfb_slate(season: Optional[int] = None, week: int = 13, team: Optional[str] = None) -> Dict[str, Any]:
    """Fetches College Football game predictions and line edges (SaturdaySlate Engine). Defaults to current year."""
    target_season = season if season else datetime.now().year
    try:
        from src.api.server import predict_week, PredictRequest
        req = PredictRequest(season=target_season, week=week, team=team)
        results = predict_week(req)
        return {"season": target_season, "week": week, "predictions": results}
    except Exception as e:
        logger.error(f"Error calling CFB predict: {e}")
        return {"error": str(e), "service": "SaturdaySlate CFB"}


def tool_get_cfb_ratings(season: Optional[int] = None) -> Dict[str, Any]:
    """Fetches dynamic Elo and Glicko-2 ratings for College Football teams (SaturdaySlate Engine). Defaults to current year."""
    target_season = season if season else datetime.now().year
    try:
        from src.api.server import get_team_ratings
        ratings = get_team_ratings(season=target_season)
        return {"season": target_season, "ratings_count": len(ratings), "ratings": [r.model_dump() for r in ratings[:15]]}
    except Exception as e:
        logger.error(f"Error calling CFB ratings: {e}")
        return {"error": str(e), "service": "SaturdaySlate CFB"}


SYSTEM_PROMPT = (
    "You are SportsMatrix AI, the primary intelligent assistant and narrative analyst for the unified sports prediction platform. "
    "You interface with 4 quantitative computation engines:\n"
    "1. Moneyball (MLB Baseball: Win probabilities, Statcast metrics, Monte Carlo simulations)\n"
    "2. NetPredict (Basketball: NBA, WNBA, NCAAM, NCAAW four-factor ratings and spreads)\n"
    "3. NoFreeLocks (NFL Football: Tabular ML ensemble, margins, totals, and situational features)\n"
    "4. SaturdaySlate (College Football: Dynamic Elo/Glicko ratings and line edge detection)\n\n"
    "As the single top-level intelligence layer, use your tools to retrieve raw quantitative data, probabilities, and news extractions. "
    "Synthesize data into clear, professional, authoritative match analyses, written narrative rationales, and player injury impact evaluations."
)


def register_agent_tools(agent: Agent):
    """Registers all 4 sport service tools with a Pydantic AI agent instance."""
    agent.tool_plain(tool_predict_mlb_slate)
    agent.tool_plain(tool_simulate_mlb_matchup)
    agent.tool_plain(tool_predict_basketball)
    agent.tool_plain(tool_predict_nfl_game)
    agent.tool_plain(tool_extract_nfl_news)
    agent.tool_plain(tool_predict_cfb_slate)
    agent.tool_plain(tool_get_cfb_ratings)
    return agent


def create_pydantic_ai_agent(settings: SettingsConfig) -> Optional[Agent]:
    """Builds a Pydantic AI Agent instance for the active provider."""
    provider = settings.active_provider.lower()
    model_name = settings.selected_model.strip()

    try:
        if provider == "openrouter":
            api_key = settings.openrouter_api_key or os.environ.get("OPENROUTER_API_KEY", "")
            if not api_key:
                return None
            p = OpenAIProvider(base_url="https://openrouter.ai/api/v1", api_key=api_key)
            m = OpenAIChatModel(model_name or "meta-llama/llama-3.3-70b-instruct", provider=p)
            agent = Agent(m, system_prompt=SYSTEM_PROMPT)
            return register_agent_tools(agent)

        elif provider == "ollama_local":
            base_url = (settings.ollama_local_base_url or "http://localhost:11434").rstrip("/") + "/v1"
            p = OpenAIProvider(base_url=base_url, api_key="ollama")
            m = OpenAIChatModel(model_name or "qwen2.5:7b", provider=p)
            agent = Agent(m, system_prompt=SYSTEM_PROMPT)
            return register_agent_tools(agent)

        elif provider == "ollama_cloud":
            base_url = (settings.ollama_cloud_base_url or "https://ollama.com").rstrip("/") + "/v1"
            api_key = settings.ollama_cloud_api_key or "ollama"
            p = OpenAIProvider(base_url=base_url, api_key=api_key)
            m = OpenAIChatModel(model_name or "qwen2.5:72b", provider=p)
            agent = Agent(m, system_prompt=SYSTEM_PROMPT)
            return register_agent_tools(agent)

        elif provider == "openai":
            api_key = settings.openai_api_key or os.environ.get("OPENAI_API_KEY", "")
            if not api_key:
                return None
            p = OpenAIProvider(api_key=api_key)
            m = OpenAIChatModel(model_name or "gpt-4o", provider=p)
            agent = Agent(m, system_prompt=SYSTEM_PROMPT)
            return register_agent_tools(agent)

        elif provider == "gemini":
            api_key = settings.gemini_api_key or os.environ.get("GEMINI_API_KEY", "")
            if not api_key:
                return None
            os.environ["GEMINI_API_KEY"] = api_key
            agent = Agent(f"google-gla:{model_name or 'gemini-1.5-flash'}", system_prompt=SYSTEM_PROMPT)
            return register_agent_tools(agent)

        elif provider == "anthropic":
            api_key = settings.anthropic_api_key or os.environ.get("ANTHROPIC_API_KEY", "")
            if not api_key:
                return None
            os.environ["ANTHROPIC_API_KEY"] = api_key
            agent = Agent(f"anthropic:{model_name or 'claude-3-5-sonnet-latest'}", system_prompt=SYSTEM_PROMPT)
            return register_agent_tools(agent)

        else: # mock / test
            return None

    except Exception as e:
        logger.warning(f"Failed to build Pydantic AI agent for {provider}: {e}")
        return None


# --- CHAT DISPATCHER ---

def process_sports_chat(req: ChatRequest) -> ChatResponse:
    """
    Main entrypoint for SportsMatrix LLM Chat queries.
    Dynamically loads settings and uses Pydantic AI for active providers or fallback tool execution.
    """
    settings = load_settings()
    today_str = datetime.now().strftime("%Y-%m-%d")
    current_year = datetime.now().year
    
    # Allow prompt-level override of model or provider if specified
    if req.model and ":" in req.model:
        parts = req.model.split(":", 1)
        settings.active_provider = parts[0]
        settings.selected_model = parts[1]

    prompt_lower = req.prompt.lower()
    tools_used: List[ToolCallLog] = []
    service_sources: List[str] = []

    # Attempt Pydantic AI Agent Execution
    agent = create_pydantic_ai_agent(settings)
    if agent is not None:
        try:
            run_result = agent.run_sync(req.prompt)
            provider_label = f"{settings.active_provider.upper()} ({settings.selected_model})"
            return ChatResponse(
                response=run_result.output,
                conversation_id=req.conversation_id or "conv_" + datetime.now().strftime("%Y%m%d_%H%M%S"),
                tools_used=[],
                service_sources=[f"Pydantic AI Agent [{provider_label}]"]
            )
        except Exception as e:
            logger.warning(f"Pydantic AI run failed for {settings.active_provider}, using fallback dispatcher: {e}")

    # Fallback Tool Execution Router Mode
    results_summary = []

    # 1. MLB / Baseball detection
    if any(k in prompt_lower for k in ["mlb", "baseball", "red sox", "yankees", "dodgers", "giants", "moneyball"]):
        service_sources.append("Moneyball (MLB)")
        if "sim" in prompt_lower or "simulate" in prompt_lower:
            sim_res = tool_simulate_mlb_matchup(home_team="LAD", away_team="SF", num_simulations=10000)
            tools_used.append(ToolCallLog(tool_name="simulate_mlb_matchup", args={"home": "LAD", "away": "SF"}, summary="Ran 10,000 Monte Carlo simulations"))
            results_summary.append(f"⚾ **MLB Monte Carlo Matchup Simulation (SF @ LAD)**:\n"
                                   f"- Home Win Prob (LAD): {sim_res.get('home_win_prob')}\n"
                                   f"- Away Win Prob (SF): {sim_res.get('away_win_prob')}\n"
                                   f"- Projected Score: {sim_res.get('expected_score')}\n"
                                   f"- Over 8.5 Runs Prob: {sim_res.get('over_8_5_prob')}")
        else:
            slate_res = tool_predict_mlb_slate(date=today_str)
            tools_used.append(ToolCallLog(tool_name="predict_mlb_slate", args={"date": today_str}, summary=f"Retrieved {slate_res.get('total_games', 0)} MLB predictions"))
            preds = slate_res.get("predictions", [])[:3]
            pred_lines = "\n".join([f"- **{p['matchup']}**: Pick **{p['model_pick']}** (Win Prob: {p['pick_win_prob']}, Proj: {p['proj_score']}, EV: {p['expected_ev']})" for p in preds])
            results_summary.append(f"⚾ **Moneyball MLB Slate Predictions ({today_str})**:\n"
                                   f"- Total Games: {slate_res.get('total_games')}\n"
                                   f"- Verified Hit Rate: {slate_res.get('hit_rate')}\n"
                                   f"- Key Matches:\n{pred_lines}")

    # 2. Basketball (NBA, WNBA, NCAAM, NCAAW) detection
    if any(k in prompt_lower for k in ["nba", "wnba", "ncaam", "ncaaw", "basketball", "hoops", "netpredict"]):
        service_sources.append("NetPredict (Basketball)")
        league = "nba"
        for lg in ["wnba", "ncaam", "ncaaw", "nba"]:
            if lg in prompt_lower:
                league = lg
                break
        bk_res = tool_predict_basketball(league=league, date=today_str)
        tools_used.append(ToolCallLog(tool_name="predict_basketball", args={"league": league, "date": today_str}, summary=f"Evaluated {bk_res.get('games_count', 0)} {league.upper()} games"))
        preds = bk_res.get("predictions", [])[:2]
        pred_lines = []
        for p in preds:
            pred_obj = p.get("prediction", {})
            pred_lines.append(f"- **Game {p.get('game_id')}**: Home Rating: {pred_obj.get('home_off_rating')}/{pred_obj.get('home_def_rating')}, Away Rating: {pred_obj.get('away_off_rating')}/{pred_obj.get('away_def_rating')}, Proj Spread: {pred_obj.get('predicted_spread')}, Proj Total: {pred_obj.get('predicted_total')}")
        results_summary.append(f"🏀 **NetPredict {league.upper()} Predictions ({today_str})**:\n"
                               f"- Odds Source: {bk_res.get('odds_source')}\n"
                               f"- Evaluated Games ({bk_res.get('games_count')}):\n" + "\n".join(pred_lines))

    # 3. NFL Football detection
    if any(k in prompt_lower for k in ["nfl", "football", "chiefs", "kc", "49ers", "eagles", "patriots", "packers", "nofreelocks", "mahomes"]):
        service_sources.append("NoFreeLocks (NFL)")
        if "news" in prompt_lower or "injury" in prompt_lower:
            news_res = tool_extract_nfl_news(req.prompt)
            tools_used.append(ToolCallLog(tool_name="extract_nfl_news", args={"text": req.prompt[:30]}, summary="Extracted player news updates"))
            results_summary.append(f"🏈 **NoFreeLocks NFL Roster & Injury News Extraction**:\n- Parsed Updates: {json.dumps(news_res.get('extracted_updates', []))}")
        else:
            nfl_res = tool_predict_nfl_game(home_team="KC", away_team="SF", vegas_spread=-2.5, vegas_total=47.5)
            tools_used.append(ToolCallLog(tool_name="predict_nfl_game", args={"home": "KC", "away": "SF"}, summary="Evaluated KC vs SF NFL matchup"))
            results_summary.append(f"🏈 **NoFreeLocks NFL Game Prediction (SF @ KC)**:\n"
                                   f"- Home Win Prob (KC): {nfl_res.get('win_probability_home')*100:.1f}%\n"
                                   f"- Predicted Margin: {nfl_res.get('predicted_margin')} pts (Vegas: {nfl_res.get('vegas_spread')})\n"
                                   f"- Predicted Total: {nfl_res.get('predicted_total')} pts (Vegas: {nfl_res.get('vegas_total')})\n"
                                   f"- LLM Narrative Rationale: {nfl_res.get('explanation', 'N/A')}")

    # 4. College Football (CFB) detection
    if any(k in prompt_lower for k in ["cfb", "college football", "saturdayslate", "sec", "big ten", "alabama", "georgia", "ohio state"]):
        service_sources.append("SaturdaySlate (CFB)")
        if "rating" in prompt_lower or "elo" in prompt_lower:
            ratings_res = tool_get_cfb_ratings(season=current_year)
            tools_used.append(ToolCallLog(tool_name="get_cfb_ratings", args={"season": current_year}, summary="Fetched CFB team ratings"))
            top_teams = ", ".join([f"{r['team']} (Elo: {r['elo_rating']})" for r in ratings_res.get("ratings", [])[:5]])
            results_summary.append(f"🏈 **SaturdaySlate CFB Team Ratings ({current_year})**:\n- Top Teams: {top_teams}")
        else:
            cfb_res = tool_predict_cfb_slate(season=current_year, week=13)
            tools_used.append(ToolCallLog(tool_name="predict_cfb_slate", args={"season": current_year, "week": 13}, summary="Generated CFB Week 13 predictions"))
            preds = cfb_res.get("predictions", [])[:3]
            pred_lines = "\n".join([f"- **{p.get('matchup', 'Game')}**: Pick **{p.get('pick', 'N/A')}** (Spread: {p.get('market_spread')}, Line Edge: {p.get('spread_edge')})" for p in preds]) if preds else "Week 13 slate analyzed."
            results_summary.append(f"🏈 **SaturdaySlate College Football Predictions (Season {current_year} Week 13)**:\n{pred_lines}")

    # If prompt is general or didn't trigger specific sport keywords, provide overview across all 4 services
    if not results_summary:
        service_sources = ["Moneyball (MLB)", "NetPredict (Basketball)", "NoFreeLocks (NFL)", "SaturdaySlate (CFB)"]
        mlb = tool_predict_mlb_slate(date=today_str)
        bk = tool_predict_basketball(league="nba", date=today_str)
        nfl = tool_predict_nfl_game(home_team="KC", away_team="SF")
        cfb = tool_get_cfb_ratings(season=current_year)

        tools_used.extend([
            ToolCallLog(tool_name="predict_mlb_slate", args={"date": today_str}, summary="MLB slate summary"),
            ToolCallLog(tool_name="predict_basketball", args={"league": "nba", "date": today_str}, summary="NBA predictions summary"),
            ToolCallLog(tool_name="predict_nfl_game", args={"home": "KC", "away": "SF"}, summary="NFL matchup summary"),
            ToolCallLog(tool_name="get_cfb_ratings", args={"season": current_year}, summary="CFB ratings summary"),
        ])

        top_cfb = ", ".join([r["team"] for r in cfb.get("ratings", [])[:3]])
        results_summary.append(
            f"Welcome to **SportsMatrix AI**! I am connected to all 4 prediction engines:\n\n"
            f"1. ⚾ **Moneyball (MLB)**: {mlb.get('total_games', 0)} slate games analyzed for {today_str} with a {mlb.get('hit_rate', 'N/A')} hit rate.\n"
            f"2. 🏀 **NetPredict (NBA/WNBA/NCAAM/NCAAW)**: Live basketball analytics covering {bk.get('games_count', 0)} NBA games for {today_str}.\n"
            f"3. 🏈 **NoFreeLocks (NFL)**: KC vs SF projected home win prob is {nfl.get('win_probability_home')*100:.1f}% with LLM explanation.\n"
            f"4. 🏈 **SaturdaySlate (College Football)**: Dynamic Elo ratings active for {current_year}. Top teams: {top_cfb}.\n\n"
            f"Ask me any question about upcoming games, spread edges, win probabilities, player injury news, or Monte Carlo simulations!"
        )

    final_text = "\n\n---\n\n".join(results_summary)
    return ChatResponse(
        response=final_text,
        conversation_id=req.conversation_id or "conv_" + datetime.now().strftime("%Y%m%d_%H%M%S"),
        tools_used=tools_used,
        service_sources=service_sources
    )
