# Architecture

## Overview

Enterprise AI Logistics Solution is a modular, containerized platform that combines a FastAPI backend, a Streamlit dashboard, and Google's Gemini 1.5 Pro to deliver AI-powered logistics insights.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                          │
│         (Streamlit Dashboard / API Consumers)                │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTPS / JSON
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     Application Layer                        │
│  ┌──────────────────────┐    ┌──────────────────────┐       │
│  │   FastAPI Backend    │    │ Streamlit Dashboard  │       │
│  │   (src/api.py)       │    │  (src/dashboard.py)  │       │
│  └──────────┬───────────┘    └──────────────────────┘       │
└─────────────┼───────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│                       Service Layer                          │
│  ┌──────────────────┐  ┌──────────────────┐                 │
│  │ src/services.py  │  │  src/utils.py    │                 │
│  │  (AI logic)      │  │  (helpers)       │                 │
│  └────────┬─────────┘  └──────────────────┘                 │
└───────────┼─────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────┐
│                      External Services                       │
│         Google Gemini 1.5 Pro API                            │
└─────────────────────────────────────────────────────────────┘
```

## Module Structure

```
src/
├── __init__.py        # Package metadata
├── api.py             # FastAPI application and routes
├── services.py        # AI business logic
├── models.py          # Pydantic schemas (request/response)
├── config.py          # Settings (env-based)
├── utils.py           # Utility/helper functions
└── dashboard.py       # Streamlit UI

tests/
├── test_models.py     # Model validation tests
├── test_api.py        # Endpoint integration tests
└── test_utils.py      # Unit tests for utilities
```

## Request Flow

1. **Client** sends a request to the FastAPI endpoint `/v1/analyze`.
2. **FastAPI** validates the request body via Pydantic models.
3. **Services layer** calls the Gemini API with structured instructions.
4. **Gemini** returns a generated response.
5. **API** formats the response and returns it to the client.
6. **Dashboard** displays the response with interactive visualizations.

## Security

- API key authentication (per-request and env-based)
- CORS middleware (configurable)
- Input validation (Pydantic)
- Secrets excluded via `.gitignore`
- Dependency scanning via GitHub Actions

## Deployment

The application is fully containerized:

- `Dockerfile` — FastAPI backend
- `Dockerfile.ui` — Streamlit dashboard
- `docker-compose.yml` — Orchestrates both services

## Scalability

- Stateless API (horizontal scaling)
- Async FastAPI handlers
- Health check endpoint for load balancers
- CORS support for multi-domain access

## Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.10+ |
| API Framework | FastAPI |
| UI Framework | Streamlit |
| AI Model | Google Gemini 1.5 Pro |
| Validation | Pydantic v2 |
| Containerization | Docker, Docker Compose |
| Testing | pytest |
| CI/CD | GitHub Actions |
