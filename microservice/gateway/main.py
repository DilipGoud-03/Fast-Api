from fastapi import FastAPI
from api.routes import bar

app =  FastAPI()


app.include_router(bar.router,prefix="/baar")