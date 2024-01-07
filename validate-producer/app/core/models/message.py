from typing import List, Optional

from pydantic import BaseModel


class Item(BaseModel):
    id: int
    quantity: int


class Message(BaseModel):
    email: str
    address: str
    items: List[Item]

    class Config:
        schema_extra = {
            "example": {
                "email": "test@gmail.com",
                "address": "Timisoara, RO",
                "items": [
                    {"id": 1, "quantity": 10},
                    {"id": 10, "quantity": 1}
                ],
            }
        }

