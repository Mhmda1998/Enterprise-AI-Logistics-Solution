"""
Enterprise AI Logistics Agent
Powered by Google Gemini 1.5 Pro
Author: Mohammed Ibrahim Ghabban
License: MIT
"""
import os
import time
import logging
from typing import List, Dict, Optional
from collections import deque

import google.generativeai as genai
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChatRequest(BaseModel):
    """Incoming chat request from API or dashboard."""
    message: str = Field(..., min_length=1, max_length=2000, description="User query")
    session_id: Optional[str] = Field(default="default", description="Conversation session")
    context: Optional[Dict] = Field(default=None, description="Optional logistics context")


class ChatResponse(BaseModel):
    """Structured response from the AI agent."""
    reply: str
    session_id: str
    tokens_used: int
    latency_ms: int
    model: str


class RateLimiter:
    """Simple sliding-window rate limiter (per session)."""

    def __init__(self, max_requests: int = 20, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window = window_seconds
        self._buckets: Dict[str, deque] = {}

    def allow(self, key: str) -> bool:
        now = time.time()
        bucket = self._buckets.setdefault(key, deque())
        # Drop entries outside the window
        while bucket and now - bucket[0] > self.window:
            bucket.popleft()
        if len(bucket) >= self.max_requests:
            return False
        bucket.append(now)
        return True


class LogisticsAgent:
    """
    Enterprise-grade AI Agent for global logistics & supply-chain intelligence.
    Capabilities:
      - Route optimization analysis
      - Cost & ETA estimation
      - Risk assessment (geopolitical, weather, customs)
      - Carrier comparison recommendations
    """

    SYSTEM_PROMPT = """You are an expert Enterprise Logistics & Supply Chain AI Agent.
You help B2B clients (shippers, 3PL providers, freight forwarders) with:
  1. Route optimization across air, sea, road, and rail
  2. Cost estimation and carrier selection
  3. Risk assessment (delays, customs, geopolitical, weather)
  4. Shipment tracking diagnostics
  5. Carbon footprint & sustainability trade-offs
Always provide structured, actionable answers. Use numbers, comparisons, and clear recommendations.
If you don't have enough data, ask clarifying questions (origin, destination, cargo type, weight, urgency)."""

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-1.5-pro"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is required. Set it in .env or pass it explicitly.")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=self.SYSTEM_PROMPT,
        )
        self.sessions: Dict[str, List[Dict]] = {}
        self.rate_limiter = RateLimiter(max_requests=20, window_seconds=60)
        self.total_tokens = 0
        logger.info(f"LogisticsAgent ready (model={model_name})")

    def _get_history(self, session_id: str) -> List[Dict]:
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        return self.sessions[session_id]

    def chat(self, request: ChatRequest) -> ChatResponse:
        """Process a chat request and return a structured response."""
        if not self.rate_limiter.allow(request.session_id):
            raise PermissionError(f"Rate limit exceeded for session '{request.session_id}'. Try again in 60s.")

        history = self._get_history(request.session_id)
        context_block = ""
        if request.context:
            context_block = "\n[Context]\n" + "\n".join(f"- {k}: {v}" for k, v in request.context.items())
        prompt = request.message + context_block

        chat_session = self.model.start_chat(history=history)
        start = time.time()
        try:
            response = chat_session.send_message(prompt)
        except Exception as exc:
            logger.exception("Gemini call failed")
            raise RuntimeError(f"AI provider error: {exc}") from exc
        latency_ms = int((time.time() - start) * 1000)

        text = response.text or ""
        usage = getattr(response, "usage_metadata", None)
        tokens = getattr(usage, "total_token_count", 0) or 0
        self.total_tokens += tokens

        # Persist the turn in session history (cap at 20 turns)
        history.append({"role": "user", "parts": [prompt]})
        history.append({"role": "model", "parts": [text]})
        if len(history) > 20:
            del history[: len(history) - 20]

        return ChatResponse(
            reply=text,
            session_id=request.session_id,
            tokens_used=tokens,
            latency_ms=latency_ms,
            model="gemini-1.5-pro",
        )

    def health(self) -> Dict:
        """Return health & usage stats for monitoring."""
        return {
            "status": "ok",
            "model": "gemini-1.5-pro",
            "active_sessions": len(self.sessions),
            "total_tokens_used": self.total_tokens,
        }
