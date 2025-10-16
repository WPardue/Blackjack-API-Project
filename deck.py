from pydantic import BaseModel

class deck(BaseModel):
    success: bool
    deck_id: str
    shuffled: bool
    remaining: int

    def __repr__(self):
        return self.deck_id