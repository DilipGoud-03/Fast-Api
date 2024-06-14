from pydantic import BaseModel,EmailStr,Field
from typing import Union

class ContactBase(BaseModel):
    first_name : Union[str,None] = Field(min_length=5 ,max_length=20)
    last_name :  Union[str,None] = Field(min_length=5 ,max_length=10)
    email : Union[EmailStr]

class CreateContact (ContactBase) :
        pass

class UserBase(BaseModel):
    first_name : Union[str,None] = Field(min_length=5 ,max_length=20)
    last_name :  Union[str,None] = Field(min_length=5 ,max_length=10)
    email : Union[EmailStr]
    password : Union[str,None] = Field(min_length=4 ,max_length=10)

class CreateUser(UserBase):
    pass