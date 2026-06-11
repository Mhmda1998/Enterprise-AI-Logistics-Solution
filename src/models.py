"""Pydantic models for API request/response validation."""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class AnalysisRequest(BaseModel):
    """Request model for logistics analysis."""

    prompt: str = Field(
        ...,
        min_length=10,
        max_length=4000,
        description="The logistics query or problem statement to analyze"
    )
    context: str = Field(
        default="",
        max_length=8000,
        description="Optional context data (JSON, CSV, or text)"
    )
    api_key: Optional[str] = Field(
        default=None,
        description="Google Gemini API key (overrides env var)"
    )

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, v: str) -> str:
        """Ensure prompt is not just whitespace."""
        if not v.strip():
            raise ValueError("Prompt cannot be empty or whitespace")
        return v.strip()


class AnalysisResponse(BaseModel):
    """Response model for logistics analysis."""

    status: str = Field(..., description="Status of the analysis")
    ai_response: str = Field(..., description="AI-generated analysis")
    developer_note: str = Field(..., description="Developer verification note")
    timestamp: Optional[str] = Field(
        default=None,
        description="ISO 8601 timestamp of the analysis"
    )


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str
    system: str
    author: str
    version: str
