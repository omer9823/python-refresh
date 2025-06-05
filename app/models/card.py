from pydantic import BaseModel


class Card(BaseModel):
    rank: str
    suit: str
    value: int
    count_value: int
