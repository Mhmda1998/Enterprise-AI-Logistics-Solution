"""AI service module for Gemini integration."""
import google.generativeai as genai
from typing import Optional

from .config import get_settings
from .utils import setup_logging, mask_api_key

logger = setup_logging()

SYSTEM_INSTRUCTIONS = (
    "You are a Senior Logistics Strategist. Your responses must be "
    "data-driven, professional, and concise. This system is part of "
    "the Enterprise AI Solution developed by Mohammed Ibrahim Ghabban."
)


def configure_gemini(api_key: Optional[str] = None) -> genai.GenerativeModel:
    """Configure the Gemini model with the provided API key."""
    settings = get_settings()
    key = api_key or settings.api_key

    if not key:
        raise ValueError("API key is required to configure Gemini")

    genai.configure(api_key=key)
    logger.info("Gemini configured with key: %s", mask_api_key(key))

    return genai.GenerativeModel(settings.gemini_model)


def build_query(prompt: str, context: str = "") -> str:
    """Build a full query string combining system instructions and user input."""
    parts = [SYSTEM_INSTRUCTIONS, ""]

    if context and context.strip():
        parts.extend(["[DATA CONTEXT]", context.strip(), ""])

    parts.extend(["[USER QUERY]", prompt])
    return "\n".join(parts)


def generate_analysis(prompt: str, context: str, api_key: Optional[str] = None) -> str:
    """Generate AI-powered logistics analysis."""
    model = configure_gemini(api_key)
    full_query = build_query(prompt, context)
    response = model.generate_content(full_query)
    return response.text
