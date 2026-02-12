import requests
from getaway.models import Trip

OLLAMA_URL = "http://localhost:11434/api/generate"
def ask_ai(user_prompt):


    # Fetch the trips from the database
    trips = Trip.objects.all()[:5] # limit the trips number to 5

    if not trips:
        trip_context = "No trips currently available."
    else:
        trip_context = "\n".join([
            f"{trip.title} | {trip.category.name} | {trip.level} | £{trip.price}"
            for trip in trips
        ])


    # System prompt
    system_prompt = f"""
You are an AI assistant for GreenGetaway.

Available Trips:
{trip_context}

Only recommend trips listed above.
Do not invent new services.

Do NOT invent trips that are not listed above.
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

        return response.json().get("response", "No response.")
    except requests.exceptions.RequestException as e:
        return f"AI communication error: {str(e)}"