from pydantic import BaseModel
from datetime import datetime

class Receita(BaseModel):
    value: float
    received: bool
    fixed: bool
    date: datetime
    category: str
    description: str