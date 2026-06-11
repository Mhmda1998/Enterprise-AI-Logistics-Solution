"""FastAPI application for the Enterprise AI Logistics Solution."""
import os
from contextlib import asynccontextmanager
from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .models import AnalysisRequest, AnalysisResponse, HealthResponse
from .services import generate_analysis
from .utils import setup_logging, get_timestamp, format_response_time

load_dotenv()
logger = setup_logging()
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management."""
    logger.info("Starting %s v%s", settings.app_name, settings.app_version)
    yield
    logger.info("Shutting down %s", settings.app_name)


app = FastAPI(
    title=settings.app_name,
    description="Enterprise-grade AI Logistics Solution powered by Gemini 1.5 Pro",
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

if settings.enable_cors:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    """Health check endpoint to verify system status."""
    return HealthResponse(
        status="Operational",
        system=settings.app_name,
        author="Mohammed Ibrahim Ghabban (GEAR Certified Developer)",
        version=settings.app_version,
    )


@app.post(
    "/v1/analyze",
    response_model=AnalysisResponse,
    tags=["Analysis"],
    status_code=status.HTTP_200_OK,
)
async def analyze_logistics(request: AnalysisRequest) -> AnalysisResponse:
    """Analyze logistics data and return AI-powered insights."""
    start_time = datetime.utcnow()
    api_key = request.api_key or os.getenv("GEMINI_API_KEY")

    if not api_key:
        logger.warning("Analysis request rejected: missing API key")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key is required. Set GEMINI_API_KEY env var or pass api_key in request.",
        )

    try:
        logger.info("Starting analysis for prompt: %s...", request.prompt[:50])
        ai_response = generate_analysis(
            prompt=request.prompt,
            context=request.context,
            api_key=api_key,
        )
        elapsed_ms = format_response_time(start_time)
        logger.info("Analysis completed in %sms", elapsed_ms)

        return AnalysisResponse(
            status="success",
            ai_response=ai_response,
            developer_note="Verified by GEAR Certified Dev: Mohammed Ghabban",
            timestamp=get_timestamp(),
        )
    except Exception as exc:
        logger.error("AI Engine Error: %s", str(exc))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI Engine Error: {str(exc)}",
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.api:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )
