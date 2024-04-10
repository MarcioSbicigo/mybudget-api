from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.models.model_category import *
from app.dependencies.database_requests import get_user_database_connection, insert_log
from app.dependencies.data_verification import verify_session
from fastapi import APIRouter

router = APIRouter()

@router.get("/api/categories")
async def load_categories(request: GetCategories):
    if verify_session(request.username, request.session_id):
        
        user_db = get_user_database_connection(request.username)
        
        if request.type_category == 'receive':
            categories = list(user_db['categorias_receita'].find({}, {'_id': 0, 'name': 1}))
            return JSONResponse(content={"Content": categories})

        if request.type_category == 'expense':
            categories = list(user_db['categorias_despesa'].find({}, {'_id': 0, 'name': 1}))
            return JSONResponse(content={"Content": categories})
    else:
        raise HTTPException(status_code=401, detail="Operation not permitted: Expired Session.")

@router.post("/api/categories")
async def insert_category(request: PostCategory):
    if verify_session(request.username, request.session_id):
        user_db = get_user_database_connection(request.username)
        
        if request.type_category == 'receive':
            existing_category = user_db['categorias_receita'].find_one({'name': request.name_category})
            
            if not existing_category:
                user_db['categorias_receita'].insert_one({'name': request.name_category})
                insert_log(f'Added receive category: {request.name_category}', 'log_operations', f'mb_{request.username}')
                
                return JSONResponse(content={"Content": "Success: Income category successfully added."})
            else:
                raise HTTPException(status_code=409, detail="Conflict: Income category already exists.")

        if request.type_category == 'expense':
            existing_category = user_db['categorias_despesa'].find_one({'name': request.name_category})
            
            if not existing_category:
                user_db['categorias_despesa'].insert_one({'name': request.name_category})
                insert_log(f'Added expense category: {request.name_category}', 'log_operations', f'mb_{request.username}')
                
                return JSONResponse(content={"Content": "Success: Expense category successfully added."})
            else:
                raise HTTPException(status_code=409, detail="Conflict: Expense category already exists.")
            
    else:
        raise HTTPException(status_code=401, detail="Operation not permitted: Expired Session.")

@router.delete("/api/categories")
def remove_category(request: DeleteCategory):
    if verify_session(request.username, request.session_id):
        user_db = get_user_database_connection(request.username)
        
        if request.type_category == 'receive':
            existing_category = user_db['categorias_receita'].find_one({'name': request.name_category})
            
            if existing_category:
                user_db['categorias_receita'].delete_one({'name': request.name_category})
                insert_log(f'Deleted receive category: {request.name_category}', 'log_operations', f'mb_{request.username}')
                
                return JSONResponse(content={"Content": "Income category successfully removed."})
            else:
                raise HTTPException(status_code=404, detail="Not found: Income category not exist.")

        if request.type_category == 'expense':
            existing_category = user_db['categorias_despesa'].find_one({'name': request.name_category})
            
            if existing_category:
                user_db['categorias_despesa'].delete_one({'name': request.name_category})
                insert_log(f'Deleted expense category: {request.name_category}', 'log_operations', f'mb_{request.username}')
                
                return JSONResponse(content={"Content": "Expense category successfully removed."})
            else:
                raise HTTPException(status_code=404, detail="Not found: Expense category not exist.")
            
    else:
        raise HTTPException(status_code=401, detail="Operation not permitted: Expired Session.")