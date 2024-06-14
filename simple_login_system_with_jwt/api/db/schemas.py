from pydantic import BaseModel, Field,EmailStr
from typing import Union

class TokenSchema(BaseModel):
    access_token: str
    
class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None

class UserBase(BaseModel):
    user_name : Union[str] = Field (min_length=4,description="user name")
    email: Union[EmailStr] = Field(description="user email")
    password: Union[str] = Field(min_length=5, max_length=24, description="user password")

class RegisterUser(UserBase):
    pass

class UserOut(BaseModel):
    id: int
    user_name :str
    email: EmailStr

class SystemUser(UserOut):
    password: str