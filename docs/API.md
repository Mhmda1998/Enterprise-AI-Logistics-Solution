# API Documentation

## Base URL

```
http://localhost:8000
```

## Authentication

All analysis endpoints require a Google Gemini API key. You can provide it in two ways:

1. **Environment variable** (recommended):
   ```bash
   export GEMINI_API_KEY=your_api_key_here
   ```

2. **Request body** (override per request):
   ```json
   { "api_key": "your_api_key_here" }
   ```

## Endpoints

### GET /

Health check endpoint.

**Response:**
```json
{
  "status": "Operational",
  "system": "Logistics AI Engine",
  "author": "Mohammed Ibrahim Ghabban (GEAR Certified Developer)",
  "version": "1.0.0"
}
```

### POST /v1/analyze

Analyzes logistics data using Gemini 1.5 Pro.

**Request body:**
```json
{
  "prompt": "Optimize delivery routes for 500 packages across 3 cities",
  "context": "Optional CSV, JSON, or descriptive text",
  "api_key": "optional_override_key"
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `prompt` | string | Yes | The logistics question (10-4000 chars) |
| `context` | string | No | Additional context (max 8000 chars) |
| `api_key` | string | No | Override env API key |

**Response (200 OK):**
```json
{
  "status": "success",
  "ai_response": "Detailed analysis from Gemini...",
  "developer_note": "Verified by GEAR Certified Dev: Mohammed Ghabban",
  "timestamp": "2026-06-11T12:00:00.000000Z"
}
```

**Error responses:**

| Code | Reason |
|------|--------|
| 401 | Missing or invalid API key |
| 422 | Validation error (prompt too short, etc.) |
| 500 | AI engine or internal error |

## Interactive Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI schema: `http://localhost:8000/openapi.json`

## Rate Limiting

Default limit: 60 requests/minute. Configurable via `RATE_LIMIT_PER_MINUTE` env var.

## Examples

See [`examples/`](../examples/) directory for usage examples.
