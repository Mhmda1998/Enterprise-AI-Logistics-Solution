"""Tests for utility functions."""
from datetime import datetime, timedelta

from src.utils import (
    get_timestamp,
    sanitize_input,
    mask_api_key,
    format_response_time,
)


class TestGetTimestamp:
    def test_returns_string(self):
        result = get_timestamp()
        assert isinstance(result, str)
        assert "T" in result
        assert result.endswith("Z")


class TestSanitizeInput:
    def test_strips_whitespace(self):
        assert sanitize_input("  hello  ") == "hello"

    def test_limits_length(self):
        long_text = "a" * 1000
        result = sanitize_input(long_text, max_length=100)
        assert len(result) == 100

    def test_empty_string(self):
        assert sanitize_input("") == ""


class TestMaskApiKey:
    def test_none_returns_none_string(self):
        assert mask_api_key(None) == "None"

    def test_short_key_masked(self):
        assert mask_api_key("abc") == "***"

    def test_long_key_partially_visible(self):
        masked = mask_api_key("abcdefghijklmnop")
        assert masked.startswith("abcd")
        assert masked.endswith("mnop")
        assert "..." in masked


class TestFormatResponseTime:
    def test_returns_milliseconds(self):
        start = datetime.utcnow() - timedelta(milliseconds=500)
        result = format_response_time(start)
        assert isinstance(result, float)
        assert result >= 500
