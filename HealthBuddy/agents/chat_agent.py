import os, json
from datetime import datetime
from agents.summary_agent import gemini_generate  # same AI function used before

class ChatAgent:
    def __init__(self, chat_dir="memory/chat"):
        self.chat_dir = chat_dir
        os.makedirs(chat_dir, exist_ok=True)

    def _get_chat_file(self, user):
        return os.path.join(self.chat_dir, f"{user}.json")

    def load_history(self, user):
        path = self._get_chat_file(user)
        if not os.path.exists(path):
            return []
        return json.load(open(path))

    def save_history(self, user, history):
        path = self._get_chat_file(user)
        json.dump(history, open(path, "w"), indent=2)

    def generate_reply(self, prompt):
        # Try Gemini if key is available
        reply = gemini_generate(prompt, language="en")
        if reply:
            return reply

        # fallback — rule based (simple)
        prompt_l = prompt.lower()

        if "amh" in prompt_l:
            return "Your AMH seems important. I can summarize your AMH report or explain the meaning."
        if "fsh" in prompt_l:
            return "FSH helps evaluate fertility and hormone balance."
        if "symptom" in prompt_l:
            return "Please describe your symptoms clearly (e.g., fatigue + dizziness)."
        return "I am here to help. Please ask about your reports, tests or symptoms."

    def run(self, user, message):
        # load past chats
        history = self.load_history(user)

        # append new user message
        history.append({
            "role": "user",
            "message": message,
            "time": datetime.utcnow().isoformat()
        })

        # create prompt for Gemini
        prompt = "\n".join(
            [f'{h["role"]}: {h["message"]}' for h in history[-6:]]  # last 6 messages
        )

        reply = self.generate_reply(prompt)

        # save assistant reply
        history.append({
            "role": "assistant",
            "message": reply,
            "time": datetime.utcnow().isoformat()
        })

        self.save_history(user, history)

        return reply
