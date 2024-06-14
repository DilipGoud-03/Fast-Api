from fastapi import FastAPI
from api.routes import user,todo

app = FastAPI()
app.include_router(user.router,tags=["Users"])
app.include_router(todo.router,tags=["Todos"])

