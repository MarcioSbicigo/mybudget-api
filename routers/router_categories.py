from fastapi import HTTPException
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
        raise HTTPException(status_code=401, detail="Operation not permitted: Expired Session.")

@router.post("/api/categories")
async def insert_category(request: PostCategorie):
    if verify_session(request.username, request.session_id):
        user_db = get_user_database_connection(request.username)
        
        if request.type_category == 'receita':
            existing_category = user_db['categorias_receita'].find_one({'name': request.name_category})
            
            if not existing_category:
                user_db['categorias_receita'].insert_one({'name': request.name_category})
                return JSONResponse(content={"Content": "Success: Income category successfully added."})
            else:
                raise HTTPException(status_code=409, detail="Conflict: Income category already exists.")

        if request.type_category == 'despesa':
            existing_category = user_db['categorias_despesa'].find_one({'name': request.name_category})
            
            if not existing_category:
                user_db['categorias_despesa'].insert_one({'name': request.name_category})
                return JSONResponse(content={"Content": "Success: Expense category successfully added."})
            else:
                raise HTTPException(status_code=409, detail="Conflict: Expense category already exists.")
            
    else:
        raise HTTPException(status_code=401, detail="Operation not permitted: Expired Session.")

@router.delete("/api/categories")
def remove_category(request: DeleteCategory):
    if verify_session(request.username, request.session_id):
        user_db = get_user_database_connection(request.username)
        
        if request.type_category == 'receita':
            existing_category = user_db['categorias_receita'].find_one({'name': request.name_category})
            
            if existing_category:
                user_db['categorias_receita'].delete_one({'name': request.name_category})
                return JSONResponse(content={"Content": "Income category successfully removed."})
            else:
                raise HTTPException(status_code=404, detail="Not found: Income category not exist.")

        if request.type_category == 'despesa':
            existing_category = user_db['categorias_despesa'].find_one({'name': request.name_category})
            
            if existing_category:
                user_db['categorias_despesa'].delete_one({'name': request.name_category})
                return JSONResponse(content={"Content": "Expense category successfully removed."})
            else:
                raise HTTPException(status_code=404, detail="Not found: Expense category not exist.")
            
    else:
        raise HTTPException(status_code=401, detail="Operation not permitted: Expired Session.")