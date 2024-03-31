from pydantic import BaseModel

class GetCategories(BaseModel):
    type_category: str
    username: str
    session_id: str
    
class PostCategory(BaseModel):
    name_category: str
    type_category: str
    username: str
    session_id: str

class DeleteCategory(BaseModel):
    name_category: str
    type_category: str
    username: str
    session_id: str