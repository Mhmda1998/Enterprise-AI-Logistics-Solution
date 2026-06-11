"""Example: How to call the Enterprise AI Logistics API."""

import os
import requests

API_URL = os.getenv("API_URL", "http://localhost:8000")
API_KEY = os.getenv("GEMINI_API_KEY", "your_api_key_here")


def analyze_logistics(prompt: str, context: str = "") -> dict:
    """Send a logistics analysis request to the API."""
    response = requests.post(
        f"{API_URL}/v1/analyze",
        json={
            "prompt": prompt,
            "context": context,
            "api_key": API_KEY,
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def check_health() -> dict:
    """Check API health status."""
    response = requests.get(f"{API_URL}/", timeout=10)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    # 1. Health check
    print("=== Health Check ===")
    health = check_health()
    print(f"Status: {health['status']}")
    print(f"Version: {health['version']}\n")

    # 2. Simple analysis
    print("=== Simple Analysis ===")
    result = analyze_logistics(
        prompt="Optimize delivery routes for 500 packages across 3 cities",
    )
    print(f"Status: {result['status']}")
    print(f"AI Response:\n{result['ai_response']}\n")

    # 3. Analysis with context (CSV-like data)
    print("=== Analysis with Context ===")
    context = """
    Route,Distance (km),Cost ($),Avg Delivery Time (hrs)
    R1,120,450,3
    R2,200,720,5
    R3,150,530,4
    """
    result = analyze_logistics(
        prompt="Identify the most cost-effective route and suggest optimizations",
        context=context,
    )
    print(f"AI Response:\n{result['ai_response']}")
