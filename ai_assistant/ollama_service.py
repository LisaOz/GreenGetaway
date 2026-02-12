import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
def ask_ai(user_prompt):

    system_prompt = """
You are an AI assistant for the GreenGetaway travel platform.

GreenGetaway only offers:
- City Strolls (short guided urban tours in London)
- Nature Retreats (short daytime nature trips)

The platform does NOT offer:
- Hotel bookings
- Accommodation packages
- Flight tickets
- Camping reservations
- External activities
- Trips outside the UK
- City strolls outside London

You must ONLY recommend city strolls and nature retreats available on the GreenGetaway platform.

If a user asks for something outside the platform services,
politely explain that GreenGetaway only provides London city strolls and nature retreats.
"""

    full_prompt = f"{system_prompt}\n\nUser: {user_prompt}\nAssistant:"

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "phi",
                "prompt": full_prompt,
                "stream": False
            },
            timeout=100
        )
        response.raise_for_status()

        return response.json().get("response", "No response from model.")
    except requests.exceptions.RequestException as e:
        return f"AI communication error: {str(e)}"