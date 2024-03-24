from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime
from models.model_requests import RegisterRequest
from dependencies.database_requests import *
from fastapi import APIRouter
from pandas import DataFrame

router = APIRouter()
register_request = RegisterRequest
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init_database_user(username):
       
    data_structure = {'Value': [0],
                      'Received': [1],
                      'Fixed': [0],
                      'Date': [datetime.datetime.strptime('1900-01-01', '%Y-%m-%d')],
                      'Category': [''],
                      'Description': ['*transacao-inicial*']}
    
    categorias_receita = ["Salário", "Rendimentos", "Vendas", "Cashback"]
    categorias_despesa = ["Alimentação", "Aluguel", "Água", "Luz", "Combustível", "Saúde", "Lazer"]
    
    db_user = get_user_database_connection(username)
    
    if db_user is not None:
        try:
            df_receitas_despesas = DataFrame(data_structure)
                        
            # Salvando o DataFrame de receitas no MongoDB
            db_user['receitas'].insert_many(df_receitas_despesas.to_dict('records'))
            db_user['despesas'].insert_many(df_receitas_despesas.to_dict('records'))
            
            # Inserindo categorias de receitas
            for categoria in categorias_receita:
                cat = {'name': categoria}
                db_user['categorias_receita'].insert_one(cat)
            
            # Inserindo categorias de despesas
            for categoria in categorias_despesa:
                cat = {'name': categoria}
                db_user['categorias_despesa'].insert_one(cat)
                
            insert_log(f'Banco de dados criado: mb_{username}.')
            
        except Exception as error:
            print(f'Erro ao inicializar banco de dados de {username}: {error}')

@router.post("/api/register")
async def register(request: register_request):
    db = get_database_connection()
    
    if db is not None:
        try:
            if 'all_users' in db.list_collection_names():
                existing_user = get_users_collection().find_one({"username": request.username})
                if existing_user:
                    raise HTTPException(status_code=400, detail="Nome de usuário já existente.")

                existing_email = get_users_collection().find_one({"email": request.email})
                if existing_email:
                    raise HTTPException(status_code=400, detail="E-mail já existente.")

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
        
    raise HTTPException(status_code=500, detail="Erro interno do servidor")
