from langchain_core.language_models import LLM
from typing import Optional, List, Mapping, Any
import requests

class DeepSeekLLM(LLM):
    api_key: str
    endpoint: str = "https://api.deepseek.com/v1/chat/completions"
    model: str = "deepseek-chat"  # or deepseek-coder or deepseek-r1
    temperature: float = 0.7
    max_tokens: int = 1024

    @property
    def _llm_type(self) -> str:
        return "deepseek-llm"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }

        response = requests.post(self.endpoint, headers=headers, json=payload)

        if response.status_code != 200:
            raise Exception(f"DeepSeek API Error: {response.status_code} - {response.text}")

        return response.json()["choices"][0]["message"]["content"]
