from pydantic import BaseModel, Field
from typing import Optional

class Item(BaseModel):
    id: Optional[int] = Field(default=None)
    name: str
    description: str
    localization: str
    date: Optional[str] = Field(default=None)
    image: str
    ticket_price: Optional[float] = Field(default=None
                                          ) 
