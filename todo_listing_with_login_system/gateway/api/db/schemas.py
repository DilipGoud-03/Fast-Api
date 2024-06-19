from pydantic import BaseModel,EmailStr,Field
from typing import Union

# Todo base class
class TodoBase(BaseModel):
    title :Union[str] = Field(default=None , min_length= 4 ,max_length=20)
    description : str

# Create new todo 
class CreateTodo(TodoBase) :
    pass
    class Config : 
        orm_mode = True

# Update todo 
class UpdateTodo (TodoBase) :
    pass

# Comment Base class
class CommentBase(BaseModel):
    comment : Union[str] = Field(default="",min_length=5 ,max_length=100)

# Create new Commnet to todo
class CreateComment(CommentBase) :
    pass

    class Config : 
        orm_mode = True   

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
    class Config : 
        orm_mode = True

class UserOut(BaseModel):
    id: int
    user_name :str
    email: EmailStr

class SystemUser(UserOut):
    pass