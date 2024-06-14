from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel,Field
from typing_extensions import Annotated

app = FastAPI()


class User(BaseModel):
    name: str
    description: Union[str, None] = None
    email: str
    age: int

    model_config = {
        "json_schema_extra":{
            "examples":[
                {
                    "name" : "Dilip",
                    "description" :"Dilip is learning fastApi by original website",
                    "email" : "dilipgaurh@gmail.com",
                    "age":22
                }
            ]
        }
    }

class Item(BaseModel):
    name: str = Field(examples=["Food"])
    description: Union[str, None] = Field(default=None, examples=["A very nice Item"])
    price: float = Field(examples=[35.4])
    tax: Union[float, None] = Field(default=None, examples=[3.2])


@app.post("/items/")
async def update_item(item: Item):
    return item

@app.put("/User/{user_id}")
async def update_user(user_id: int, user: User):
    results = {"user_id": user_id, "user": user}
    return results

