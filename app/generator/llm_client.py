import requests
import os

OLLAMA_URL = os.getenv("OLLAMA_API", "https://tcfzj9r3teosn0-11434.proxy.runpod.net")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3")
print(f"Using OLLAMA API at {OLLAMA_URL}")

def generate_response(prompt: str):
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
        return response.json()["response"]
    except requests.RequestException as e:
        print("Error while calling Ollama API:", e)
        return "Error: Failed to get a response from Ollama."
