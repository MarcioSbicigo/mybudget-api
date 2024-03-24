import datetime
from pymongo import MongoClient
from config import Secrets

mongo_uri = Secrets.MONGO_URI
app_db_name = Secrets.APP_DB_NAME
users_collection = Secrets.USERS_COLLECTION
sessions_collection = Secrets.SESSIONS_COLLECTION

def get_database_connection():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        # db = client[app_db_name]
        db = client['MyBudget']
        
        return db
    
    except Exception as error:
        print(f'Erro ao acessar database principal: {error}')
        return None

def get_user_database_connection(username: str):
    try:
        client = MongoClient("mongodb://localhost:27017/")
        database_name = f'mb_{username}'
        
        db = client[database_name]
        
        return db
    
    except Exception as error:
        print(f'Erro ao acessar database {database_name}: {error}')
        return None

def get_users_collection():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        # db = client[app_db_name]
        db = client['MyBudget']
        users_collection = db['all_users']
        
        return users_collection
    
    except Exception as error:
        print(f'Erro ao acessar collection de usuários: {error}')
        return None

def get_sessions_collection():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        # db = client['STD_DB_NAME']
        db = client['MyBudget']
        sessions_collection = db['all_sessions']
        
        return sessions_collection
    
    except Exception as error:
        print(f'Erro ao acessar collection de sessões: {error}')
        return None

def insert_log(event: str, collection='log_aplicacao', database_name='MyBudget'):
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client[database_name]
        
        app_log = db[collection]
        datetime_log = datetime.datetime.now()
        log = {'Evento': event, 'timestamp': datetime_log}
        app_log.insert_one(log)
    
    except Exception as error:
            print(f'Erro ao inserir log: {error}')

