"""
SportsMatrix LLM Provider Settings Manager & Persistence Module
"""

import os
import json
import logging
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

CONFIG_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "sportsmatrix_config.json"))


class SettingsConfig(BaseModel):
    active_provider: str = Field("openrouter", description="Active LLM provider: openrouter, ollama_local, ollama_cloud, openai, gemini, anthropic, mock")
    selected_model: str = Field("meta-llama/llama-3.3-70b-instruct", description="Selected model name for current provider")
    openrouter_api_key: str = Field("", description="OpenRouter API Key")
    ollama_local_base_url: str = Field("http://localhost:11434", description="Local Ollama Server Base URL")
    ollama_cloud_base_url: str = Field("https://ollama.com", description="Ollama Cloud Server Base URL")
    ollama_cloud_api_key: str = Field("", description="Ollama Cloud API Key")
    openai_api_key: str = Field("", description="OpenAI API Key")
    gemini_api_key: str = Field("", description="Google Gemini API Key")
    anthropic_api_key: str = Field("", description="Anthropic API Key")


def load_settings() -> SettingsConfig:
    """Loads settings from sportsmatrix_config.json or environment variables."""
    if os.path.exists(CONFIG_FILE_PATH):
        try:
            with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return SettingsConfig(**data)
        except Exception as e:
            logger.error(f"Error loading config file {CONFIG_FILE_PATH}: {e}")

    # Fallback from environment variables
    openrouter_key = os.environ.get("OPENROUTER_API_KEY", "")
    openai_key = os.environ.get("OPENAI_API_KEY", "")
    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")

    provider = "mock"
    model = "test"
    if openrouter_key:
        provider = "openrouter"
        model = "meta-llama/llama-3.3-70b-instruct"
    elif openai_key:
        provider = "openai"
        model = "gpt-4o"
    elif gemini_key:
        provider = "gemini"
        model = "gemini-1.5-flash"
    elif anthropic_key:
        provider = "anthropic"
        model = "claude-3-5-sonnet-latest"

    return SettingsConfig(
        active_provider=provider,
        selected_model=model,
        openrouter_api_key=openrouter_key,
        openai_api_key=openai_key,
        gemini_api_key=gemini_key,
        anthropic_api_key=anthropic_key
    )


def save_settings(config: SettingsConfig) -> None:
    """Persists settings to sportsmatrix_config.json."""
    try:
        with open(CONFIG_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(config.model_dump(), f, indent=2)
        logger.info(f"Successfully saved settings to {CONFIG_FILE_PATH}")
    except Exception as e:
        logger.error(f"Failed to save settings: {e}")
