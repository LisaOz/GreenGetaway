import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def ask_ai(prompt):
    payload = {
        "model": "phi",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        return response.json()["response"]
    else:
        return "Error communicating with AI"
