from typing import List, Optional, Dict
from pydantic import BaseModel, field_validator

class Card(BaseModel):
    image: str
    value: str
    suit: str
    code: str

class Pile(BaseModel):
    cards: Optional[List[Card]] = None
    remaining: int

    # Convert string "remaining" values (e.g. "3") to int
    @field_validator("remaining", mode="before")
    def parse_remaining(cls, v):
        return int(v)

class hand(BaseModel):
    success: bool
    deck_id: str
    remaining: int
    piles: Dict[str, Pile]

    @field_validator("remaining", mode="before")
    def parse_remaining(cls, v):
        return int(v)