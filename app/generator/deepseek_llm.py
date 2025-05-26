import requests

def generate_response(prompt: str):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "deepseek-coder:1.3b",
            "prompt": prompt,
            "stream": False
        }
    )
    response.raise_for_status()
    return response.json()["response"]
