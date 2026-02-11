from django.shortcuts import render
from .ollama_service import ask_ai

# Create your views here.

def ai_chat(request):
    response_text = None

    if request.method == "POST":
        user_prompt = request.POST.get("prompt")
        response_text = ask_ai(user_prompt)

    return render (request, "ai_assistant/chat.html", {
        "response": response_text
    })