from os import environ

# Local: mongodb://localhost:27017/
# Docker: mongodb://mongodb:27017/

# Export Linux: export MONGO_URI='mongodb://localhost:27017/myBudget'
# Export Windows: $Env:MONGO_URI = "mongodb://localhost:27017/myBudget"

class Secrets:
    
    # SECRET_KEY = environ.get("SECRET_KEY")
    
    # MONGO_URI = environ.get("MONGO_URI")
    
    # APP_DB_NAME = environ.get("APP_DB_NAME")
    
    # USERS_COLLECTION = environ.get("USERS_COLLECTION")
    # SESSIONS_COLLECTION = environ.get("SESSIONS_COLLECTION")
    
    SECRET_KEY = "Eu4Ug%I_DIPr90["
    
    MONGO_URI = "mongodb://localhost:27017/"
    
    APP_DB_NAME = "MyBudget"
    
    USERS_COLLECTION = "all_users"
    SESSIONS_COLLECTION = "all_sessions"
