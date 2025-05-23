from typing import List, Optional
from langchain_core.language_models.llms import LLM
from pydantic import BaseModel, Field
from openai import OpenAI


class DeepSeekRouterLLM(LLM):
    model: str = "deepseek/deepseek-prover-v2:free"
    api_key: str
    base_url: str = "https://openrouter.ai/api/v1"
    temperature: float = 0.7
    site_url: Optional[str] = None
    site_title: Optional[str] = None

    # internal use only (not fields)
    client: OpenAI = Field(default=None, exclude=True)
    headers: dict = Field(default_factory=dict, exclude=True)

    def __init__(self, **data):
        super().__init__(**data)

        # Setup OpenAI client
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )

        # Setup headers if provided
        if self.site_url:
            self.headers["HTTP-Referer"] = self.site_url
        if self.site_title:
            self.headers["X-Title"] = self.site_title

    @property
    def _llm_type(self) -> str:
        return "deepseek-router"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            extra_headers=self.headers,
            extra_body={},
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
        )
        return response.choices[0].message.content
