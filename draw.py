from pydantic import BaseModel
from typing import List

class CardImages(BaseModel):
    svg: str
    png: str

class Card(BaseModel):
    code: str
    image: str
    images: CardImages
    value: str
    suit: str

class draw(BaseModel):
    success: bool
    deck_id: str
    cards: List[Card]
    remaining: int

    def __repr__(self):
        return self.deck_id