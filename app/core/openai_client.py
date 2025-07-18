from fastapi import Depends
from openai import AsyncOpenAI, OpenAIError

from .config import Settings, get_settings


class OpenAIClient:
    """Thin wrapper around the async OpenAI SDK."""

    def __init__(self, settings: Settings = Depends(get_settings)) -> None:
        self._client = AsyncOpenAI(api_key=settings.openai_api_key)
        self._model = settings.openai_model

    async def simplify_bill(self, text: str) -> str:
        system = (
            "You are a friendly medical-billing assistant. "
            "Convert complex line-item charges into plain-language "
            "explanations suitable for a non-technical patient."
        )

        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": text},
                ],
                temperature=0.2,
                max_tokens=512,
            )

            return response.choices[0].message.content.strip()
        except OpenAIError as exc:  # pragma: no cover
            raise RuntimeError("OpenAI request failed") from exc
