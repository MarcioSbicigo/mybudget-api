from fastapi import HTTPException
from fastapi.responses import JSONResponse
from bson.objectid import ObjectId
from app.models.model_auth_requests import LogoutRequest
from app.dependencies.database_requests import get_users_collection, get_sessions_collection
from fastapi import APIRouter

router = APIRouter()

@router.post("/api/logout")
async def login(request: LogoutRequest):
    try:    
        user = get_users_collection().find_one({"username": request.username})
        
        if not user:
            raise HTTPException(status_code=401, detail="Usuário inválido.")
        
        else:
            get_sessions_collection().delete_one({"username": user["username"]})
            
            return JSONResponse(content={"Status": "Successful logout"})
    except Exception as error:
        print(f'Logout route error: {error}')
        raise HTTPException(status_code=500, detail="Internal error from logout route.")