from fastapi import HTTPException
from fastapi.responses import JSONResponse
from bson.objectid import ObjectId
import uuid
from datetime import datetime, timedelta
from models.model_requests import LoginRequest
from dependencies.database_requests import get_users_collection, get_sessions_collection
from dependencies.data_verification import *
from fastapi import APIRouter

router = APIRouter()

@router.post("/api/login")
async def login(request: LoginRequest):

    user = get_users_collection().find_one({"username": request.username})
    
    # Verificando se o usuário existe no banco de dados ou se a senha está incorreta
    if not user or not verify_password(request.password, user["password"]):
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos.")
    
    # Verificando se a sessão do usuário existe nas sessões ativas
    existing_session = get_sessions_collection().find_one({"session_id": user["session_id"]})

    if existing_session:
        # Verificar se a sessão já expirou
        expiration_time = datetime.strptime(existing_session["expire_time"], '%Y-%m-%d %H:%M:%S')
        current_time = datetime.now()
        
        if current_time > expiration_time:
            # Se a sessão expirou, remove a sessão existente e gera uma nova
            get_sessions_collection().delete_one({"username": user["username"]})
        else:
            # Se a sessão ainda está ativa, gera um token com as informações existentes
            user_data = {
                "username": user["username"],
                "email": user["email"],
                "full_name": user["full_name"],
                "session_id": existing_session["session_id"]
            }
            token = create_token(user_data)
            
            return JSONResponse(content={"Status": "Successful login", "access_token": token})
        
    session_id = str(uuid.uuid4())
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    expire_time = datetime.now() + timedelta(hours=2)
    expire_time = expire_time.strftime('%Y-%m-%d %H:%M:%S')

    session = {
        'username': user["username"],
        'session_id': session_id,
        'login_time': current_time,
        'expire_time': expire_time
    }
    
    # Atualiza o session_id e a data do último login no objeto do do usuário
    get_users_collection().update_one({"_id": ObjectId(user["_id"])}, {"$set": {"session_id": session_id}})
    get_users_collection().update_one({"_id": ObjectId(user["_id"])}, {"$set": {"last_login": current_time}})
    
    # Insere uma nova sessão
    get_sessions_collection().insert_one(session)
    
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