from typing import List, Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.post("/items/")
async def create_item(item: Item):
    return item


@app.get("/items/")
async def read_items() -> List[Item]:
    return [
        Item(name="Portal Gun", price=42.0,tax=20.50),
        Item(name="Plumbus", price=32.0,tax=20.50),
    ] 