from pydantic import BaseModel

class GetCategorie(BaseModel):
    type_category: str
    username: str
    session_id: str
    
class PostCategorie(BaseModel):
    name_category: str
    type_category: str
    username: str
    session_id: str
