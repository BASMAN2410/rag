import os
import requests

OLLAMA_URL = os.getenv("OLLAMA_API", "http://localhost:11434")
print(f"Using OLLAMA API at {OLLAMA_URL}")
def generate_response(prompt: str):
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )
    response.raise_for_status()
    return response.json()["response"]