from passlib.context import CryptContext
from datetime import datetime
from app.dependencies.database_requests import get_sessions_collection
from config import Secrets

secret_key = Secrets.SECRET_KEY

def verify_password(plain_password, hashed_password):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)

def verify_session(username: str, session_id: str):
    try:
        existing_session = get_sessions_collection().find_one({"username": username})
        if existing_session and existing_session["session_id"] == session_id:
            expiration_time = datetime.strptime(existing_session["expire_time"], '%Y-%m-%d %H:%M:%S')
            current_time = datetime.now()
            return True if (current_time < expiration_time) else None
        else:
            return None
    except Exception as error:
        print(f'Erro ao verificar sessão: {error}')