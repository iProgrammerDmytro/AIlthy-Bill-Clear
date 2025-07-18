from pydantic import BaseModel, Field


class SimplifyRequest(BaseModel):
    text: str = Field(
        ..., min_length=5, max_length=8_000, example="CPT 99213 - Office Visit"
    )


class SimplifyResponse(BaseModel):
    result: str
