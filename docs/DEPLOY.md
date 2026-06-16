# 🚀 One-Click Deployment Guide

The fastest way to get **Enterprise AI Logistics** live on the internet is to use the included `render.yaml` Blueprint.

## Option 1: Render (recommended, free tier)

1. Sign up / log in at **[render.com](https://render.com)**
2. Go to **Blueprints** → **New Blueprint Instance**
3. Connect your GitHub account and select this repository
4. Render will read `render.yaml` and create **two services**:
   - `enterprise-logistics-api` → `https://enterprise-logistics-api.onrender.com`
   - `enterprise-logistics-dashboard` → `https://enterprise-logistics-dashboard.onrender.com`
5. When prompted, set the `GEMINI_API_KEY` env var (get one free at [aistudio.google.com/apikey](https://aistudio.google.com/apikey))
6. Wait ~3 minutes for the first build. Done. 🎉

> Free tier caveat: Render spins down the service after 15 min of inactivity. The first request takes ~30s to wake up.

## Option 2: Railway

1. Sign up at **[railway.app](https://railway.app)**
2. **New Project** → **Deploy from GitHub repo** → select this repository
3. Add a service, set the start command to:
   ```
   uvicorn api.server:app --host 0.0.0.0 --port $PORT
   ```
4. Add `GEMINI_API_KEY` and `API_KEYS` env vars
5. Deploy.

## Option 3: Plain Docker

```bash
docker build -f Dockerfile -t logistics-api .
docker run -p 8000:8000 --env-file .env logistics-api

# in another shell
docker build -f Dockerfile.ui -t logistics-ui .
docker run -p 8501:8501 \
  -e API_URL=http://host.docker.internal:8000 \
  -e API_KEY=demo-key-123 \
  logistics-ui
```

## Verifying the deploy

```bash
# Health
curl https://your-api.onrender.com/health

# Ask the agent
curl -X POST https://your-api.onrender.com/v1/chat \
  -H "X-API-Key: demo-key-123" \
  -H "Content-Type: application/json" \
  -d '{"message":"Plan a shipment from Dubai to Hamburg for 5 tons of textiles."}'
```

## Costs

| Service | Render Free | Render Starter | Railway Hobby |
|---|---|---|---|
| API | $0 (sleeps after 15 min) | $7/mo | $5 credit/mo |
| Dashboard | $0 (sleeps) | $7/mo | included |
| Gemini API | Free tier: 15 RPM | Pay-as-you-go | Same |

For a portfolio demo, **Render free is plenty**.
