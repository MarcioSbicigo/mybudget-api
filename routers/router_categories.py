from fastapi.responses import JSONResponse
from models.model_category import *
from dependencies.database_requests import get_user_database_connection
from dependencies.data_verification import verify_session
from fastapi import APIRouter

router = APIRouter()

@router.get("/api/categories")
async def load_categories(request: GetCategorie):
    if verify_session(request.username, request.session_id):
        
        user_db = get_user_database_connection(request.username)
        
        if request.type_category == 'receita':
            categories = list(user_db['categorias_receita'].find({}, {'_id': 0, 'nome': 1}))
            return JSONResponse(content={"Content": categories})

        if request.type_category == 'despesa':
            categories = list(user_db['categorias_despesa'].find({}, {'_id': 0, 'nome': 1}))
            return JSONResponse(content={"Content": categories})
    else:
        return JSONResponse(content={"Content": "error"})
    
    
@router.post("/api/categories")
async def insert_category(request: PostCategorie):
    if verify_session(request.username, request.session_id):
        user_db = get_user_database_connection(request.username)
        
        if request.type_category == 'receita':
            user_db['categorias_receita'].insert_one({'name': request.name_category})
            return JSONResponse(content={"Content": "Category successfully added."})

        if request.type_category == 'despesa':
            user_db['categorias_despesa'].insert_one({'name': request.name_category})
            return JSONResponse(content={"Content": "Category successfully added."})
            
    else:
        return JSONResponse(content={"Content": "error"})