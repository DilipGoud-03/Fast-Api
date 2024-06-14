from pydantic import BaseModel,EmailStr,Field
from typing import Union

# Todo base class
class TodoBase(BaseModel):
    title :Union[str] = Field(default="",min_length=3 ,max_length=20)
    description : Union[str] = Field(default="",min_length=10 ,max_length=100)

# Create new todo 
class CreateTodo(TodoBase) :
    pass

# Update todo 
class UpdateTodo (TodoBase) :
    pass

# Comment Base class
class CommentBase(BaseModel):
    comment : Union[str] = Field(default="",min_length=5 ,max_length=100)

# Create new Commnet to todo
class CreateComment(CommentBase) :
    pass

# User
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