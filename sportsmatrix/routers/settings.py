"""
FastAPI Router for SportsMatrix Settings & LLM Model Discovery (/api/v1/settings)
"""

import logging
import httpx
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Query, HTTPException
from sportsmatrix.chatbot.settings import SettingsConfig, load_settings, save_settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/settings", tags=["Settings & LLM Discovery"])


@router.get("", response_model=SettingsConfig)
def get_current_settings():
    """Returns current SportsMatrix LLM provider & API key settings."""
    return load_settings()


@router.post("", response_model=SettingsConfig)
def update_settings(config: SettingsConfig):
    """Updates and persists SportsMatrix LLM provider settings."""
    save_settings(config)
    return config


@router.get("/models")
def fetch_available_models(
    provider: str = Query("openrouter", description="Provider ID: openrouter, ollama_local, ollama_cloud, openai, gemini, anthropic, mock"),
    openrouter_api_key: Optional[str] = Query(None),
    ollama_local_base_url: Optional[str] = Query("http://localhost:11434"),
    ollama_cloud_base_url: Optional[str] = Query("https://ollama.com"),
    ollama_cloud_api_key: Optional[str] = Query(None)
):
    """Dynamically fetches available models for the selected provider (OpenRouter, Ollama, OpenAI, etc.)."""
    provider_lower = provider.lower()

    if provider_lower == "openrouter":
        try:
            headers = {}
            if openrouter_api_key:
                headers["Authorization"] = f"Bearer {openrouter_api_key}"
            
            resp = httpx.get("https://openrouter.ai/api/v1/models", headers=headers, timeout=8.0)
            if resp.status_code == 200:
                data = resp.json()
                raw_models = [m["id"] for m in data.get("data", [])]
                
                # Highlight top featured models
                top_models = [
                    "meta-llama/llama-3.3-70b-instruct",
                    "anthropic/claude-3.5-sonnet",
                    "openai/gpt-4o",
                    "deepseek/deepseek-r1",
                    "google/gemini-2.0-flash-001",
                    "qwen/qwen-2.5-72b-instruct"
                ]
                ordered = [m for m in top_models if m in raw_models] + [m for m in raw_models if m not in top_models]
                return {"provider": "openrouter", "count": len(ordered), "models": ordered[:100]}
        except Exception as e:
            logger.warning(f"Failed to fetch live OpenRouter models: {e}")
        
        # Fallback list if network request fails
        return {
            "provider": "openrouter",
            "count": 6,
            "models": [
                "meta-llama/llama-3.3-70b-instruct",
                "anthropic/claude-3.5-sonnet",
                "openai/gpt-4o",
                "deepseek/deepseek-r1",
                "google/gemini-2.0-flash-001",
                "qwen/qwen-2.5-72b-instruct"
            ]
        }

    elif provider_lower == "ollama_local":
        base_url = (ollama_local_base_url or "http://localhost:11434").rstrip("/")
        try:
            resp = httpx.get(f"{base_url}/api/tags", timeout=3.0)
            if resp.status_code == 200:
                data = resp.json()
                models = [m["name"] for m in data.get("models", [])]
                if models:
                    return {"provider": "ollama_local", "count": len(models), "models": models}
        except Exception as e:
            logger.info(f"Local Ollama daemon not reachable at {base_url}: {e}")

        # Fallback list of common local models
        return {
            "provider": "ollama_local",
            "count": 6,
            "models": [
                "qwen2.5:7b",
                "llama3.1:8b",
                "mistral:7b",
                "deepseek-r1:8b",
                "gemma2:9b",
                "phi4:14b"
            ],
            "note": f"Offline default list. Ensure Local Ollama is running at {base_url}."
        }

    elif provider_lower == "ollama_cloud":
        base_url = (ollama_cloud_base_url or "https://ollama.com").rstrip("/")
        headers = {}
        if ollama_cloud_api_key:
            headers["Authorization"] = f"Bearer {ollama_cloud_api_key}"
        try:
            resp = httpx.get(f"{base_url}/api/tags", headers=headers, timeout=5.0)
            if resp.status_code == 200:
                data = resp.json()
                models = [m["name"] for m in data.get("models", [])]
                if models:
                    return {"provider": "ollama_cloud", "count": len(models), "models": models}
        except Exception as e:
            logger.info(f"Ollama Cloud endpoint check failed: {e}")

        return {
            "provider": "ollama_cloud",
            "count": 5,
            "models": [
                "qwen2.5:72b",
                "llama3.3:70b",
                "deepseek-v3",
                "mistral-large",
                "phi4:14b"
            ]
        }

    elif provider_lower == "openai":
        return {
            "provider": "openai",
            "count": 4,
            "models": ["gpt-4o", "gpt-4o-mini", "o3-mini", "gpt-4-turbo"]
        }

    elif provider_lower == "gemini":
        return {
            "provider": "gemini",
            "count": 3,
            "models": ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"]
        }

    elif provider_lower == "anthropic":
        return {
            "provider": "anthropic",
            "count": 3,
            "models": ["claude-3-5-sonnet-latest", "claude-3-5-haiku-latest", "claude-3-opus-latest"]
        }

    else: # mock / test
        return {
            "provider": "mock",
            "count": 1,
            "models": ["test-model"]
        }
