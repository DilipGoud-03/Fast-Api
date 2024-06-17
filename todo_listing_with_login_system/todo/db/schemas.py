from pydantic import BaseModel,EmailStr,Field
from typing import Union

# Todo base class
class TodoBase(BaseModel):
    title :str
    description : str

# Create new todo 
class CreateTodo(TodoBase) :
    user_id : int
    pass
    class Config : 
        from_attributes = True

# Update todo 
class UpdateTodo (TodoBase) :
    pass

# Comment Base class
class CommentBase(BaseModel):
    comment : str

# Create new Commnet to todo
class CreateComment(CommentBase) :
    user_id : int
    todo_id : int
    pass
    class Config : 
        from_attributes = True   
