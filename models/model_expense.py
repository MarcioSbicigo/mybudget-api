from pydantic import BaseModel
from datetime import datetime

class Despesa(BaseModel):
    value: float
    received: bool
    fixed: bool
    date: datetime
    category: str
    description: str
