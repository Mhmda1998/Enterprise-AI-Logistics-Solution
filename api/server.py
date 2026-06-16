"""
Enterprise AI Logistics API
FastAPI server exposing the LogisticsAgent over HTTP.
"""
import os
import secrets
import logging
from contextlib import asynccontextmanager
from typing import Dict

from fastapi import FastAPI, HTTPException, Depends, Security, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from pydantic import BaseModel

from core.agent import LogisticsAgent, ChatRequest, ChatResponse

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("api")

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

VALID_KEYS: Dict[str, str] = {}  # populated on startup from env


def _load_keys() -> None:
    raw = os.getenv("API_KEYS", "demo-key-123:demo-client")
    for pair in raw.split(","):
        pair = pair.strip()
        if not pair or ":" not in pair:
            continue
        key, name = pair.split(":", 1)
        VALID_KEYS[key.strip()] = name.strip()
    if not VALID_KEYS:
        VALID_KEYS["demo-key-123"] = "demo-client"
    logger.info("Loaded %d API key(s)", len(VALID_KEYS))


async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """Validate the X-API-Key header and return the client name."""
    if api_key in VALID_KEYS:
        return VALID_KEYS[api_key]
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API key. Provide a valid X-API-Key header.",
    )


@asynccontextmanager
async def lifespan(_: FastAPI):
    _load_keys()
    app.state.agent = LogisticsAgent()
    logger.info("API startup complete")
    yield
    logger.info("API shutdown")


app = FastAPI(
    title="Enterprise AI Logistics API",
    description=(
        "B2B API for autonomous logistics intelligence. "
        "Powered by Google Gemini 1.5 Pro. Use the X-API-Key header to authenticate."
    ),
    version="0.1.0",
    contact={"name": "Mohammed Ibrahim Ghabban", "url": "https://github.com/Mhmda1998"},
    license_info={"name": "MIT"},
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthResponse(BaseModel):
    status: str
    version: str
    agent: Dict


class StatsResponse(BaseModel):
    total_tokens: int
    active_sessions: int


@app.get("/", tags=["meta"])
def root() -> Dict:
    return {
        "service": "Enterprise AI Logistics API",
        "version": "0.1.0",
        "docs": "/docs",
        "openapi": "/openapi.json",
    }


@app.get("/health", response_model=HealthResponse, tags=["meta"])
def health() -> HealthResponse:
    agent = app.state.agent
    h = agent.health()
    return HealthResponse(status="ok", version="0.1.0", agent=h)


@app.get("/v1/stats", response_model=StatsResponse, tags=["meta"], dependencies=[Depends(verify_api_key)])
def stats() -> StatsResponse:
    agent = app.state.agent
    return StatsResponse(
        total_tokens=agent.total_tokens,
        active_sessions=len(agent.sessions),
    )


@app.post(
    "/v1/chat",
    response_model=ChatResponse,
    tags=["logistics"],
    summary="Ask the AI Logistics Agent",
    dependencies=[Depends(verify_api_key)],
)
def chat(request: ChatRequest) -> ChatResponse:
    try:
        return app.state.agent.chat(request)
    except PermissionError as exc:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=str(exc))
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.server:app", host="0.0.0.0", port=int(os.getenv("PORT", "8000")), reload=False)
