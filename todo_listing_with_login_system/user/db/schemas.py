from pydantic import BaseModel,EmailStr,Field
from typing import Union


class UserBase(BaseModel):
    user_name : Union[str] = Field (min_length=4,description="user name")
    email: Union[EmailStr] = Field(description="user email")
    password: Union[str] = Field(min_length=5, max_length=24, description="user password")

class RegisterUser(UserBase):
    pass
    class Config : 
        orm_model = True