from fastapi import HTTPException
from fastapi.responses import JSONResponse
from bson.objectid import ObjectId
import uuid
from datetime import datetime, timedelta
from app.models.model_auth_requests import LoginRequest, SessionStatusRequest
from app.dependencies.database_requests import get_users_collection, get_sessions_collection
from app.dependencies.data_verification import *
from fastapi import APIRouter
import jwt

router = APIRouter()

def create_token(data: dict):
    encoded_jwt = jwt.encode(data, secret_key, algorithm="HS256")
    return encoded_jwt

@router.post("/api/login")
async def login(request: LoginRequest):
    try:
        user = get_users_collection().find_one({"username": request.username})
        
        # Verificando se o usuário existe no banco de dados ou se a senha está incorreta
        if not user or not verify_password(request.password, user['password']):
            raise HTTPException(status_code=401, detail="Invalid username or password.")
        
        # Verificando se a sessão do usuário já existe nas sessões ativas
        if verify_session(user['username'], user['session_id']):
            user_data = {
                "username": user["username"],
                "email": user["email"],
                "full_name": user["full_name"],
                "session_id": user["session_id"]
                }
            
            token = create_token(user_data)
                
            return JSONResponse(content={"Status": "Successful login", "access_token": token})
        else:
            get_sessions_collection().delete_one({"username": user["username"]})
                
            session_id = str(uuid.uuid4())
            
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            expire_time = datetime.now() + timedelta(hours=2)
            expire_time = expire_time.strftime('%Y-%m-%d %H:%M:%S')

            new_session = {
                'username': user["username"],
                'session_id': session_id,
                'login_time': current_time,
                'expire_time': expire_time
            }
            
            # Atualiza o session_id e a data do último login no objeto do do usuário
            get_users_collection().update_one({"_id": ObjectId(user["_id"])}, {"$set": {"session_id": session_id}})
            get_users_collection().update_one({"_id": ObjectId(user["_id"])}, {"$set": {"last_login": current_time}})
            
            # Insere uma nova sessão
            get_sessions_collection().insert_one(new_session)
            
            # Gera os dados contidos no token de retorno
            user_data = {
                "username": user["username"],
                "email": user["email"],
                "full_name": user["full_name"],
                "session_id": session_id
            }
            
            # Cria o token jwt
            token = create_token(user_data)
            
            # Retorna o token
            return JSONResponse(content={"Status": "Successful login", "access_token": token})
    except Exception as error:
        print(f'Authentication route error: {error}')
        raise HTTPException(status_code=500, detail="Internal error from authentication route.")
    
# Rota que verifica se a sessão do usuário é válida
@router.get('/api/session')
async def register(request: SessionStatusRequest):
    session = verify_session(request.username, request.session_id)
    
    if session:
        return JSONResponse(content={"Status": "Valid session."})
    else:
        raise HTTPException(status_code=401, detail="Invalid session or expired.")