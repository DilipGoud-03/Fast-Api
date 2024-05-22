from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import Union
from typing_extensions import Annotated
app = FastAPI()

class  Items(BaseModel):
    id : int
    name : str
    quantity : int
    price : int

items = {"foo": "The Foo Wrestlers"}

# @app.get('/items/{item_id}')
# async def read_items(item_id : int) :
