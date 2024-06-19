from pydantic import BaseModel,EmailStr,Field,field_validator
from typing import Union

# Todo base class
class TodoBase(BaseModel):
    title :Union[str] = Field(default= '' , min_length= 4 ,max_length=20)
    description : Union[str] = Field(default= '' , min_length= 10 ,max_length=50)

    @field_validator("title","description")
    def strip_whitespaces(cls, v: str) -> str:
        return v.strip()


# Create new todo 
class CreateTodo(TodoBase) :
    pass
    class Config : 
        from_attributes = True

# Update todo 
class UpdateTodo (BaseModel) :
    title : Union[str,None] = Field(default= '' )
    description : Union[str,None] = Field(default= '')

    @field_validator("title","description")
    def strip_whitespaces(cls, v: str) -> str:
        return v.strip()


# Comment Base class
class CommentBase(BaseModel):
    comment : Union[str] = Field(default= '',min_length=5 ,max_length=100)

    @field_validator("comment")
    def strip_whitespaces(cls, v: str) -> str:
        return v.strip()

# Create new Commnet to todo
class CreateComment(CommentBase) :
    pass

    class Config : 
        from_attributes = True   

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

    @field_validator("user_name","email","password")
    def strip_whitespaces(cls, v: str) -> str:
        return v.strip()

class RegisterUser(UserBase):
    pass
    class Config : 
        from_attributes = True

class UserOut(BaseModel):
    id: int
    user_name :str
    email: EmailStr

class SystemUser(UserOut):
    pass