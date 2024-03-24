from fastapi import HTTPException
from fastapi.responses import JSONResponse
from bson.objectid import ObjectId
from models.model_requests import LogoutRequest
from dependencies.database_requests import get_users_collection, get_sessions_collection
from fastapi import APIRouter

router = APIRouter()

@router.post("/api/logout")
async def login(request: LogoutRequest):
    user = get_users_collection().find_one({"username": request.username})
    
    if not user:
        raise HTTPException(status_code=401, detail="Usuário inválido.")
    
    else:
        get_users_collection().update_one({"_id": ObjectId(user["_id"])}, {"$set": {"session_id": ''}})
        get_sessions_collection.delete_one({"username": user["username"]})
        
        return JSONResponse(content={"Status": "Successful logout"})