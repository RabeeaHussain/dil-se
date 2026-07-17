import importlib.util
import os
from dotenv import load_dotenv

if importlib.util.find_spec("groq") is not None:  # pragma: no cover - optional dependency path
    from groq import Groq
else:
    Groq = None

load_dotenv()

SYSTEM_PROMPT = """
You are Dil Se, a compassionate mental wellness companion for Pakistani youth.
Be warm, real, non-judgmental, and conversational.
"""

class DilSeChatbot:

    def __init__(self):
        api_key = os.getenv("AI_API_KEY")
        if not api_key:
            raise ValueError("AI_API_KEY not set")
        if Groq is None:
            raise ValueError("groq package is not installed")
        self.client = Groq(api_key=api_key)

    def get_response(self, message, language="english", conversation_history=None):
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        if conversation_history:
            messages.extend(conversation_history)

        messages.append({"role": "user", "content": message})

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=1000
        )

        return response.choices[0].message.content

    def get_quick_replies(self, language="english"):
        if language.lower() == "hinglish":
            return [
                "Main stressed hoon",
                "Mujhe baat karni hai",
                "Mujhe samajh nahi aa raha"
            ]
        return [
            "I'm stressed",
            "I need someone to talk to",
            "I feel overwhelmed"
        ]

def create_chatbot():
    return DilSeChatbot()