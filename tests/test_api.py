"""Tests for the FastAPI endpoints."""
from unittest.mock import patch, MagicMock

import pytest
from fastapi.testclient import TestClient

from src.api import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    def test_health_check_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_health_check_contains_author(self, client):
        response = client.get("/")
        data = response.json()
        assert "Mohammed" in data["author"]
        assert data["status"] == "Operational"

    def test_health_check_contains_version(self, client):
        response = client.get("/")
        data = response.json()
        assert "version" in data


class TestAnalyzeEndpoint:
    """Tests for the analyze endpoint."""

    def test_analyze_missing_api_key_returns_401(self, client):
        with patch.dict("os.environ", {}, clear=True):
            response = client.post(
                "/v1/analyze",
                json={"prompt": "Optimize shipping routes for our fleet"},
            )
        assert response.status_code == 401

    def test_analyze_short_prompt_returns_422(self, client):
        response = client.post(
            "/v1/analyze",
            json={"prompt": "short"},
        )
        assert response.status_code == 422

    @patch("src.api.generate_analysis")
    def test_analyze_success(self, mock_generate, client):
        mock_generate.return_value = "Use route optimization algorithm X."

        with patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"}):
            response = client.post(
                "/v1/analyze",
                json={"prompt": "Optimize shipping routes for 500 packages"},
            )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "ai_response" in data
        assert "timestamp" in data

    @patch("src.api.generate_analysis")
    def test_analyze_with_ai_error_returns_500(self, mock_generate, client):
        mock_generate.side_effect = Exception("AI service unavailable")

        with patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"}):
            response = client.post(
                "/v1/analyze",
                json={"prompt": "Optimize shipping routes for 500 packages"},
            )

        assert response.status_code == 500


class TestDocumentation:
    """Tests for API documentation availability."""

    def test_openapi_schema_available(self, client):
        response = client.get("/openapi.json")
        assert response.status_code == 200
        assert "paths" in response.json()

    def test_docs_endpoint_available(self, client):
        response = client.get("/docs")
        assert response.status_code == 200

    def test_redoc_endpoint_available(self, client):
        response = client.get("/redoc")
        assert response.status_code == 200
