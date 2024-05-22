from typing import Union
from typing_extensions import Annotated

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()

class UserBase(BaseModel):
    username: str
    email: EmailStr
    
class UserIn(UserBase):
    password: str
   
class UserOut(UserBase):
    pass

class UserInDB(UserBase):
    hashed_password :str
   

def generate_hashed_password(raw_password: str):
    return "supersecret" + raw_password

@app.post("/create_user/",response_model=UserOut,status_code=200)
def save_user_db(user_in:UserIn):
    hashed_password = generate_hashed_password(user_in.password)
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


