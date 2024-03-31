from pydantic import BaseModel
from datetime import datetime

class GetReceives(BaseModel):
    username: str
    session_id: str

class PostReceive(BaseModel):
    username: str
    session_id: str
    value: float
    received: bool
    fixed: bool
    date: datetime
    category: str
    description: str