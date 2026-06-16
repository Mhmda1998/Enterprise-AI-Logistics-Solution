"""
Demo video script generator.
Records a terminal-based walkthrough of the system without needing a real API key.

Usage:
    python scripts/demo.py
"""
import os
import time
import textwrap


SCRIPT = r"""
================================================================
 ENTERPRISE AI LOGISTICS SOLUTION - LIVE DEMO (text mode)
================================================================

[1/4] PROJECT OVERVIEW
  name        : Enterprise AI Logistics Solution
  audience    : B2B (shippers, 3PLs, freight forwarders)
  ai brain    : Google Gemini 1.5 Pro
  api         : FastAPI + Pydantic v2
  dashboard   : Streamlit
  container   : Docker + Render Blueprint
  ci          : GitHub Actions (pytest, 3 Python versions)

[2/4] ONE-LINER INSTALL
  $ pip install -r requirements.txt
  $ cp .env.example .env  # add GEMINI_API_KEY

[3/4] RUN THE API
  $ uvicorn api.server:app --host 0.0.0.0 --port 8000
  INFO:     Uvicorn running on http://0.0.0.0:8000
  INFO:     Application startup complete.
  $ curl http://localhost:8000/health
  {"status":"ok","version":"0.1.0","agent":{"status":"ok","model":"gemini-1.5-pro"}}

[4/4] ASK THE LOGISTICS AGENT
  $ curl -X POST http://localhost:8000/v1/chat \
      -H "X-API-Key: demo-key-123" \
      -H "Content-Type: application/json" \
      -d '{"message":"Compare sea vs air freight from Shanghai to Rotterdam for 20 tons of electronics, urgent."}'

  RESPONSE (latency ~1.8s):
  > For 20 t of electronics Shanghai -> Rotterdam with urgent SLA:
  > - Air: ~$90,000, 3-4 days transit, high CO2
  > - Sea: ~$16,000, 28 days transit, low CO2
  > Recommended hybrid: air out (3 days) + consolidation return via sea
  >   saves ~25% vs pure air, meets urgent delivery SLA on the outbound leg.

  Tokens: 612   Latency: 1840ms   Model: gemini-1.5-pro

================================================================
 END OF DEMO - repo: github.com/Mhmda1998/Enterprise-AI-Logistics-Solution
================================================================
"""


def main() -> None:
    width = 80
    if os.getenv("DEMO_SLOW", "0") == "1":
        for line in SCRIPT.splitlines():
            print(line[:width])
            time.sleep(0.03)
    else:
        print("\n".join(textwrap.fill(line, width=width) if line else "" for line in SCRIPT.splitlines()))


if __name__ == "__main__":
    main()
