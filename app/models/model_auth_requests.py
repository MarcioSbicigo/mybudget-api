from pydantic import BaseModel

class RegisterRequest(BaseModel):
    username: str
    full_name: str
    email: str
    password: str
    
class LoginRequest(BaseModel):
    username: str
    password: str
    
class LogoutRequest(BaseModel):
    username: str
    session_id: str

class SessionStatusRequest(BaseModel):
    username: str
    session_id: str