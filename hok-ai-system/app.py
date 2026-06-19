"""
HOK-AI System - GitHub App Automation
Autonomous AI-powered GitHub operations
"""
import os
import json
import logging
from typing import Dict, List, Optional

import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("hok-ai")


class HOKAISystem:
    """
    GitHub App automation system.
    Uses GitHub App authentication (JWT) to perform actions.
    """

    def __init__(self, app_id: str, private_key_path: str, installation_id: str):
        self.app_id = app_id
        self.private_key_path = private_key_path
        self.installation_id = installation_id
        self.app_token = self._get_app_token()
        self.installation_token = self._get_installation_token()

    def _get_app_token(self) -> str:
        """Generate JWT token for the GitHub App."""
        import jwt
        from datetime import datetime, timedelta

        with open(self.private_key_path, "r") as f:
            private_key = f.read()

        payload = {
            "iat": int(datetime.utcnow().timestamp()),
            "exp": int((datetime.utcnow() + timedelta(minutes=10)).timestamp()),
            "iss": self.app_id,
        }

        token = jwt.encode(payload, private_key, algorithm="RS256")
        return token

    def _get_installation_token(self) -> str:
        """Get installation access token."""
        url = f"https://api.github.com/app/installations/{self.installation_id}/access_tokens"
        headers = {
            "Authorization": f"Bearer {self.app_token}",
            "Accept": "application/vnd.github.v3+json",
        }

        response = httpx.post(url, headers=headers)
        response.raise_for_status()
        return response.json()["token"]

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"token {self.installation_token}",
            "Accept": "application/vnd.github.v3+json",
        }

    # --- Issues Operations ---

    def create_issue(self, repo: str, title: str, body: str) -> Dict:
        """Create a new issue."""
        url = f"https://api.github.com/repos/{repo}/issues"
        headers = self._get_headers()
        data = {"title": title, "body": body}

        response = httpx.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def comment_on_issue(self, repo: str, issue_number: int, body: str) -> Dict:
        """Add a comment to an issue."""
        url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
        headers = self._get_headers()
        data = {"body": body}

        response = httpx.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    # --- Pull Request Operations ---

    def create_pr(self, repo: str, title: str, body: str, head: str, base: str) -> Dict:
        """Create a new pull request."""
        url = f"https://api.github.com/repos/{repo}/pulls"
        headers = self._get_headers()
        data = {
            "title": title,
            "body": body,
            "head": head,
            "base": base,
        }

        response = httpx.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def comment_on_pr(self, repo: str, pr_number: int, body: str) -> Dict:
        """Add a comment to a pull request."""
        url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/comments"
        headers = self._get_headers()
        data = {"body": body}

        response = httpx.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    # --- Repository Operations ---

    def list_issues(self, repo: str, state: str = "open") -> List[Dict]:
        """List issues in a repository."""
        url = f"https://api.github.com/repos/{repo}/issues?state={state}"
        headers = self._get_headers()

        response = httpx.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def list_prs(self, repo: str, state: str = "open") -> List[Dict]:
        """List pull requests in a repository."""
        url = f"https://api.github.com/repos/{repo}/pulls?state={state}"
        headers = self._get_headers()

        response = httpx.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    # --- Webhook Handler (for server) ---

    def handle_webhook(self, payload: Dict, signature: str) -> Dict:
        """Handle incoming webhook events."""
        event_type = payload.get("action") or payload.get("type")
        logger.info(f"Received webhook: {event_type}")

        # Example: Auto-comment on new issues
        if event_type == "opened" and payload.get("issue"):
            issue = payload["issue"]
            repo = payload["repository"]["full_name"]
            self.comment_on_issue(
                repo,
                issue["number"],
                f"👋 Thanks for opening this issue! The HOK-AI system has been notified."
            )

        return {"status": "processed"}


if __name__ == "__main__":
    # Example usage
    hok_ai = HOKAISystem(
        app_id=os.getenv("GITHUB_APP_ID"),
        private_key_path=os.getenv("GITHUB_PRIVATE_KEY_PATH"),
        installation_id=os.getenv("GITHUB_INSTALLATION_ID"),
    )

    # Create an issue
    issue = hok_ai.create_issue(
        repo="Mhmda1998/Enterprise-AI-Logistics-Solution",
        title="[HOK-AI] New feature request",
        body="Please add support for DHL API integration.",
    )
    print(f"Created issue: {issue['html_url']}")
