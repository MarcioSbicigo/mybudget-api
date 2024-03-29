from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime
from models.model_requests import RegisterRequest
from dependencies.database_requests import *
from fastapi import APIRouter

router = APIRouter()
register_request = RegisterRequest
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init_database_user(username):
    
    data_structure = {
        'date': datetime.datetime.now(),
        'description': '*transacao-inicial*'
        }

    categorias_receita = ["Salário", "Rendimentos", "Vendas", "Cashback"]
    categorias_despesa = ["Alimentação", "Aluguel", "Água", "Luz", "Combustível", "Saúde", "Lazer"]
    
    user_db = get_user_database_connection(username)
    
    if user_db is not None:
        try:
            user_db['receitas'].insert_one(data_structure)
            user_db['despesas'].insert_one(data_structure)
            
            # Inserindo categorias de receitas
            for categoria in categorias_receita:
                cat = {'name': categoria}
                user_db['categorias_receita'].insert_one(cat)
            
            # Inserindo categorias de despesas
            for categoria in categorias_despesa:
                cat = {'name': categoria}
                user_db['categorias_despesa'].insert_one(cat)
                
            insert_log(f'Database created: mb_{username}.')
            
        except Exception as error:
            print(f'Error initializing {username} database: {error}')

@router.post("/api/register")
async def register(request: register_request):
    db = get_database_connection()
    
    if db is not None:
        try:
            if 'all_users' in db.list_collection_names():
                existing_user = get_users_collection().find_one({"username": request.username})
                if existing_user:
                    raise HTTPException(status_code=400, detail="Username already exist.")

                existing_email = get_users_collection().find_one({"email": request.email})
                if existing_email:
                    raise HTTPException(status_code=400, detail="E-mail already exist.")

            hashed_password = pwd_context.hash(request.password)

            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            new_user = {
                "username": request.username,
                "full_name": request.full_name,
                "email": request.email,
                "password": hashed_password,
                "session_id": '',
                "last_login": '',
                "register_date": current_time
            }

            get_users_collection().insert_one(new_user)
                
            init_database_user(request.username)

            return {"message": f"Usuário registrado com sucesso: {request.username}"}
        
        except HTTPException as http_error:
            print(f"\nErro ao cadastrar usuário: {request.username}\nStatus code {http_error}\n")
            raise http_error
        
    print(f'Register route error: Application database not exist.')
    raise HTTPException(status_code=500, detail="Internal Server error")
