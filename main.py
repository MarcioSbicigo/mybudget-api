from fastapi import FastAPI
from routers import router_login, router_logout, router_register, router_categories#, router_expenses, router_receives
from datetime import datetime
from dependencies.database_requests import get_database_connection
import uvicorn
from os import environ
from passlib.context import CryptContext

app = FastAPI()

app.include_router(router_register.router)
app.include_router(router_login.router)
app.include_router(router_logout.router)
app.include_router(router_categories.router)
# app.include_router(router_expenses.router)
# app.include_router(router_receives.router)

@app.get('/')
def inicializacao() -> str:
    return 'API inicilizada!'

if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run(app, port=8000)
