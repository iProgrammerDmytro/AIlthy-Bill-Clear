from fastapi import Depends

from app.core.openai_client import OpenAIClient

from .schemas import SimplifyRequest


class BillService:
    def __init__(self, llm: OpenAIClient = Depends(OpenAIClient)) -> None:
        self.llm = llm

    async def simplify(self, payload: SimplifyRequest) -> str:
        return await self.llm.simplify_bill(payload.text)
