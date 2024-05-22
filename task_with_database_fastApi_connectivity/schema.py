from pydantic import BaseModel,Field
from typing import  Union ,List


class SubTaskBase(BaseModel) :
    name : str
    description: Union[str,None] = None

class SubTaskCreate(SubTaskBase):
    pass


class SubTask(SubTaskBase):
    id :int
    task_id : int
    class Config () :
        orm_mode = True


class TaskBase(BaseModel):
    name: str = Field(examples=["your task name"])
    description: Union[str,None] = Field(default=None, examples=["your description"])
    task_status: Union[str,None] = "Pendding"

    
class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id : int
    sub_task : List[SubTask] = []
    class Config:
        orm_mode = True