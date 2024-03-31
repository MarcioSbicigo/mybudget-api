from fastapi import FastAPI
from app.routers import router_login, router_logout, router_register, router_categories, router_data
import uvicorn

app = FastAPI()

app.include_router(router_register.router)
app.include_router(router_login.router)
app.include_router(router_logout.router)
app.include_router(router_categories.router)
app.include_router(router_data.router)

@app.get('/')
def inicializacao() -> str:
    return 'API inicilizada!'

if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run(app, port=8000)
