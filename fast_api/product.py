from typing import Optional

from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
