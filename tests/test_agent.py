"""Unit tests for the LogisticsAgent. Mocks the Gemini provider so no real API key is needed."""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Ensure repo root is on the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.agent import LogisticsAgent, ChatRequest, ChatResponse, RateLimiter


class FakeResponse:
    text = "Mocked AI reply: Use sea freight to save 40%."
    usage_metadata = MagicMock(total_token_count=42)


class FakeChatSession:
    def send_message(self, _prompt):
        return FakeResponse()


class FakeModel:
    def start_chat(self, history=None):
        return FakeChatSession()


class TestRateLimiter(unittest.TestCase):
    def test_allows_under_limit(self):
        rl = RateLimiter(max_requests=3, window_seconds=60)
        for _ in range(3):
            self.assertTrue(rl.allow("s1"))

    def test_blocks_over_limit(self):
        rl = RateLimiter(max_requests=2, window_seconds=60)
        self.assertTrue(rl.allow("s1"))
        self.assertTrue(rl.allow("s1"))
        self.assertFalse(rl.allow("s1"))

    def test_separate_sessions(self):
        rl = RateLimiter(max_requests=1, window_seconds=60)
        self.assertTrue(rl.allow("s1"))
        self.assertTrue(rl.allow("s2"))
        self.assertFalse(rl.allow("s1"))


class TestChatRequestValidation(unittest.TestCase):
    def test_requires_message(self):
        with self.assertRaises(Exception):
            ChatRequest(message="")

    def test_max_length(self):
        with self.assertRaises(Exception):
            ChatRequest(message="x" * 3000)


class TestLogisticsAgent(unittest.TestCase):
    @patch("core.agent.genai.GenerativeModel")
    @patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"})
    def setUp(self, mock_model_cls):
        mock_model_cls.return_value = FakeModel()
        self.agent = LogisticsAgent()

    def test_health(self):
        h = self.agent.health()
        self.assertEqual(h["status"], "ok")
        self.assertIn("model", h)

    def test_chat_returns_response(self):
        req = ChatRequest(message="Plan a shipment from Shanghai to Rotterdam")
        resp = self.agent.chat(req)
        self.assertIsInstance(resp, ChatResponse)
        self.assertEqual(resp.tokens_used, 42)
        self.assertIn("Mocked", resp.reply)

    def test_history_persists(self):
        req = ChatRequest(message="Hello", session_id="sess-A")
        self.agent.chat(req)
        self.assertIn("sess-A", self.agent.sessions)
        self.assertGreater(len(self.agent.sessions["sess-A"]), 0)

    def test_rate_limit(self):
        req = ChatRequest(message="x", session_id="rl-test")
        with patch.object(self.agent.rate_limiter, "allow", return_value=False):
            with self.assertRaises(PermissionError):
                self.agent.chat(req)


if __name__ == "__main__":
    unittest.main()
