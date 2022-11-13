from typing import List
from pydantic import BaseModel


class TwitterResult(BaseModel):
    segment: str
    frequency: int


class TwitterResponse(BaseModel):
    original_query: str
    results: List[TwitterResult] = []
