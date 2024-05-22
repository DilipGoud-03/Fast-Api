from pydantic import BaseModel
from typing import Union,List
from enum import Enum

class Tags(str,Enum):
    todo = "ToDo",
    task = "ToDo Task"


class TodoTaskBase(BaseModel) :

    name : str
    description: Union[str,None] = None
    completed : bool = False

class CreateToDoTask(TodoTaskBase):
    pass

class TodoTask(TodoTaskBase):
    id :int
    class Config () :
        orm_mode = False

class ToDoBase(BaseModel):
    title :str
    description : str = None
    completed : bool=False

class ToDoCreate(ToDoBase):
    pass
    todo_tasks :List[CreateToDoTask]


class ToDo(ToDoBase):
    id : int
    todo_tasks :List[TodoTask]
    class Config:
        orm_mode = True
