from django.shortcuts import render
from .ollama_service import ask_ai
import logging

# Create your views here.

# Use logging to display user inputs - system responses
logger = logging.getLogger("ai_security")

def ai_chat(request):
    response_text = None

    if request.method == "POST":
        user_prompt = request.POST.get("prompt")
        response_text = ask_ai(user_prompt)

        # Log user input
        logger.warning(f"AI User Prompt: {user_prompt}")
        response_text = ask_ai(user_prompt)

        # Log AI response
        logger.warning(f"AI Model Response: {response_text}")

    return render (request, "ai_assistant/chat.html", {
        "response": response_text
    })