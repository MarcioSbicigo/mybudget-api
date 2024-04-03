import datetime
from pymongo import MongoClient
from app.config import Secrets

def get_database_connection():
    try:
        client = MongoClient(Secrets.MONGO_URI)
        db = client[Secrets.APP_DB_NAME]
        
        return db
    
    except Exception as error:
        print(f'Error accessing main database: {error}')
        return None

def get_user_database_connection(username: str):
    try:
        client = MongoClient(Secrets.MONGO_URI)
        database_name = f'mb_{username}'
        
        db = client[database_name]
        
        return db
    
    except Exception as error:
        print(f'Error accessing user database {database_name}: {error}')
        return None

def get_users_collection():
    try:
        client = MongoClient(Secrets.MONGO_URI)
        db = client[Secrets.APP_DB_NAME]
        users_collection = db[Secrets.USERS_COLLECTION]
        
        return users_collection
    
    except Exception as error:
        print(f'Error accessing users collection: {error}')
        return None

def get_sessions_collection():
    try:
        client = MongoClient(Secrets.MONGO_URI)
        db = client[Secrets.APP_DB_NAME]
        sessions_collection = db[Secrets.SESSIONS_COLLECTION]
        
        return sessions_collection
    
    except Exception as error:
        print(f'Error accessing sessions collection: {error}')
        return None

def insert_log(event: str, collection="log_api", database_name=Secrets.APP_DB_NAME):
    try:
        client = MongoClient(Secrets.MONGO_URI)
        db = client[database_name]
        
        app_log = db[collection]
        datetime_log = datetime.datetime.now()
        log = {'Evento': event, 'timestamp': datetime_log}
        app_log.insert_one(log)
    
    except Exception as error:
        print(f'Error inserting log: {error}')

