"""Utility functions for the Enterprise AI Logistics Solution."""
import logging
import sys
from datetime import datetime
from typing import Optional


def setup_logging(level: str = "INFO") -> logging.Logger:
    """Configure application-wide logging."""
    logger = logging.getLogger("logistics_ai")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def get_timestamp() -> str:
    """Get current ISO 8601 timestamp."""
    return datetime.utcnow().isoformat() + "Z"


def sanitize_input(text: str, max_length: int = 8000) -> str:
    """Sanitize user input by stripping and limiting length."""
    sanitized = text.strip()
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    return sanitized


def mask_api_key(api_key: Optional[str]) -> str:
    """Mask an API key for safe logging."""
    if not api_key:
        return "None"
    if len(api_key) <= 8:
        return "***"
    return f"{api_key[:4]}...{api_key[-4:]}"


def format_response_time(start_time: datetime) -> float:
    """Calculate response time in milliseconds."""
    delta = datetime.utcnow() - start_time
    return round(delta.total_seconds() * 1000, 2)
