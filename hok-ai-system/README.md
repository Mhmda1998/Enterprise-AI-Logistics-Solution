# 🤖 HOK-AI System

Autonomous AI-powered GitHub automation system.

## Features

- ✅ Create/Close Issues automatically
- ✅ Comment on Issues & Pull Requests
- ✅ List Issues & PRs
- ✅ Handle Webhooks
- ✅ JWT-based GitHub App authentication

## Setup

1. Create a GitHub App:
   - Go to [GitHub Settings → Developer Settings → GitHub Apps → New GitHub App](https://github.com/settings/apps/new)
   - Copy the **App ID** and **Private Key**

2. Install the App on your repository:
   - Go to [Settings → Apps → Install a new app](https://github.com/settings/apps/installations)
   - Select your repository and click "Install"

3. Configure environment variables:
   ```bash
cp .env.example .env
# Edit .env with your App ID, Private Key, and Installation ID
```

4. Run the automation:
   ```bash
pip install -r requirements.txt
python app.py
```

## Example Usage

```python
from app import HOKAISystem

hok_ai = HOKAISystem(
    app_id="12345",
    private_key_path="./private-key.pem",
    installation_id="67890",
)

# Create an issue
issue = hok_ai.create_issue(
    repo="Mhmda1998/Enterprise-AI-Logistics-Solution",
    title="[HOK-AI] Bug report",
    body="Found a bug in the agent.",
)
print(f"Created issue: {issue['html_url']}")
```

## Webhook Server (Optional)

For webhook handling, use a simple HTTP server:

```python
from fastapi import FastAPI, Request
from app import HOKAISystem

app = FastAPI()
hok_ai = HOKAISystem(...)

@app.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()
    signature = request.headers.get("X-Hub-Signature-256")
    return hok_ai.handle_webhook(payload, signature)
```

## License

MIT
