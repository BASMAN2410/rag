import requests
import os

OLLAMA_URL = os.getenv("OLLAMA_API", "http://localhost:11434").rstrip("/")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3")

print(f"[llm_client] Using OLLAMA API at {OLLAMA_URL}")

def generate_response(prompt: str) -> str:
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=20
        )
        response.raise_for_status()
        return response.json().get("response", "")
    except requests.RequestException as e:
        print("[llm_client] Error calling Ollama:", e)
        return "Error: Failed to get a response from Ollama."
