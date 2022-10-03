from pydantic import BaseModel

class TwitterRequest(BaseModel):
    query: str
    selected_text: str
    amount_multiplier: int
