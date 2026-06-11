"""Tests for Pydantic models."""
import pytest
from pydantic import ValidationError

from src.models import AnalysisRequest, AnalysisResponse, HealthResponse


class TestAnalysisRequest:
    """Tests for the AnalysisRequest model."""

    def test_valid_request(self):
        request = AnalysisRequest(prompt="Optimize shipping routes for 500 packages")
        assert request.prompt == "Optimize shipping routes for 500 packages"
        assert request.context == ""
        assert request.api_key is None

    def test_request_with_context(self):
        request = AnalysisRequest(
            prompt="Plan warehouse layout",
            context="Warehouse size: 10000 sqm",
            api_key="test-key",
        )
        assert request.context == "Warehouse size: 10000 sqm"
        assert request.api_key == "test-key"

    def test_prompt_stripped(self):
        request = AnalysisRequest(prompt="  Optimize routes  ")
        assert request.prompt == "Optimize routes"

    def test_empty_prompt_fails(self):
        with pytest.raises(ValidationError):
            AnalysisRequest(prompt="")

    def test_whitespace_prompt_fails(self):
        with pytest.raises(ValidationError):
            AnalysisRequest(prompt="          ")

    def test_short_prompt_fails(self):
        with pytest.raises(ValidationError):
            AnalysisRequest(prompt="short")

    def test_long_prompt_fails(self):
        with pytest.raises(ValidationError):
            AnalysisRequest(prompt="a" * 4001)


class TestAnalysisResponse:
    """Tests for the AnalysisResponse model."""

    def test_valid_response(self):
        response = AnalysisResponse(
            status="success",
            ai_response="Use route A for fast delivery",
            developer_note="Verified",
            timestamp="2026-06-11T12:00:00Z",
        )
        assert response.status == "success"
        assert response.timestamp == "2026-06-11T12:00:00Z"

    def test_response_without_timestamp(self):
        response = AnalysisResponse(
            status="success",
            ai_response="Response text",
            developer_note="Note",
        )
        assert response.timestamp is None


class TestHealthResponse:
    """Tests for the HealthResponse model."""

    def test_valid_health_response(self):
        health = HealthResponse(
            status="Operational",
            system="Logistics AI",
            author="Mohammed Ghabban",
            version="1.0.0",
        )
        assert health.status == "Operational"
        assert health.version == "1.0.0"
