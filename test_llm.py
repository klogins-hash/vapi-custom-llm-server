#!/usr/bin/env python3
"""
Test script for the Vapi Custom LLM Server
Tests the /chat/completions endpoint
"""

import requests
import json
import sys

# Configuration
SERVER_URL = "https://vapi-custom-llm-server-production.up.railway.app"
HEALTH_ENDPOINT = f"{SERVER_URL}/health"
CHAT_ENDPOINT = f"{SERVER_URL}/chat/completions"

def test_health():
    """Test the health check endpoint"""
    print("Testing /health endpoint...")
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_chat_completion():
    """Test the chat completions endpoint"""
    print("\nTesting /chat/completions endpoint...")

    payload = {
        "messages": [
            {
                "role": "user",
                "content": "Hello! Can you introduce yourself?"
            }
        ],
        "model": "gpt-3.5-turbo",
        "temperature": 0.7,
        "max_tokens": 150
    }

    print(f"Request payload: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(CHAT_ENDPOINT, json=payload, timeout=30)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"\nAssistant Response:")
            print(result["choices"][0]["message"]["content"])
            print(f"\nTokens used: {result['usage']['total_tokens']}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("=== Vapi Custom LLM Server Test ===\n")

    health_ok = test_health()

    if health_ok:
        chat_ok = test_chat_completion()
        sys.exit(0 if chat_ok else 1)
    else:
        print("\nHealth check failed. Server may not be running or accessible.")
        sys.exit(1)
