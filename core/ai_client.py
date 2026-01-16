# core/ai_client.py
import requests


class AIClient:
    def __init__(self, api_url: str, model: str, api_key: str = None, language: str = "ru"):
        self.api_url = api_url.rstrip('/')
        self.model = model
        self.language = language
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
        self.history = []

    def _get_system_prompt(self) -> str:
        lang_instruction = "Отвечай строго на русском языке." if self.language == "ru" else "Отвечай на английском языке."
        return (
            f"Ты — эксперт по информационной безопасности и этичному пентесту. "
            f"{lang_instruction} "
            "Ты помогаешь пользователю анализировать системы, находить уязвимости и обучаться. "
            "Все действия должны быть легальными и подтверждёнными. "
            "Если нужно выполнить команду — предложи её в формате: ```bash\nкоманда\n```"
            "Если для выполнения команды нужны права root то сообщи об этом сразу, и сразу предложи команду с sudo"
        )

    def send_message(self, user_msg: str) -> str:
        self.history.append({"role": "user", "content": user_msg})

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self._get_system_prompt()},
                *self.history
            ],
            "temperature": 0.3
        }

        try:
            resp = requests.post(
                f"{self.api_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=90
            )
            resp.raise_for_status()
            ai_reply = resp.json()["choices"][0]["message"]["content"]
            self.history.append({"role": "assistant", "content": ai_reply})
            return ai_reply
        except Exception as e:
            return f"[Ошибка подключения к ИИ: {e}]"