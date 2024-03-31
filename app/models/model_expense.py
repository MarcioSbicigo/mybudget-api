from pydantic import BaseModel
from datetime import datetime

class GetExpenses(BaseModel):
    username: str
    session_id: str
    
class PostExpense(BaseModel):
    username: str
    session_id: str
    value: float
    received: bool
    fixed: bool
    date: datetime
    category: str
    description: str
