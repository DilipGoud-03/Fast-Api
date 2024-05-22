from fastapi import FastAPI,Path,Query
from enum import Enum
from pydantic import Field,BaseModel
from typing_extensions import Annotated
from fastapi.responses import JSONResponse
from typing import Union
import datetime
import json

app = FastAPI()


class Status (str,Enum) :
    Pandding ='Pendding'
    Completed = 'Completed'

class SubTask (BaseModel):
    subTaskname : str
    description : str

class Task(BaseModel) :
    name : Union[str,None] = Field(description="name must have at least 5 charaters",min_length=5,max_length=10)
    description : Union[str,None] = Field(description="Description must have at least 10 charaters",min_length=10,max_length=100)
    status : Union[Status,None]= Field(description="Status will be Pandding or Completed")
    subTask : Union[SubTask,None] = None

task_data = "task.json"

@app.get("/task/{task_id}")
async def get_task(task_id : Annotated[int,Path(gt=0,description="Id must be an integer value")]):
    task_file = open(task_data, 'r+')
    tasks = json.load(task_file)

    
    filetterd_task = [task for task in tasks if task["id"] == task_id ]
    if  filetterd_task:
        return filetterd_task
    else :
        return JSONResponse(status_code=404, content={"message": "Task id not found"})

@app.get("/filteredTask")
def get_filterd_task (q : Annotated[Union[str,None],Query(description="Filtere by status 'Pandding or Completed' and sort by task name",min_length=5,max_length=10)]) :
    global task_data
    task_file = open(task_data, 'r+')
    tasks = json.load(task_file)
    filetterd_task = [task for task in tasks if task["name"] == q and task["status"] == q ]
    if filetterd_task :
        return filetterd_task
    else : 
        return JSONResponse(status_code=404, content={"message": "Task data not found"})
 
        
@app.post("/createTask",response_model=Task)
async def create_new_task (task_value :Task) :
    global task_data
    with open(task_data,'r+') as tasks:
        task = json.load(tasks)
        id = 1
        date = str(datetime.datetime.now())
        if task :
            id= len(task)+1
        new_task ={
            "id" : id,
            "name": task_value.name,
            "description": task_value.description,
            "status": task_value.status,
            "createdAt": date,
            "updatedAt": date,
            "subTask" : {
                "subTaskname":task_value.subTask.subTaskname,
                "description":task_value.subTask.description,
            }
        }
        task.append(new_task)
        tasks.seek(0)
        json.dump(task, tasks, indent = 8)
        return new_task


@app.put("/updateTask/{task_id}")
async def update_task (task_id :Annotated[int,Path(gt=0,description="Id must be an integer value")],task_value : Task) :
    global task_data
    with open(task_data,'r+') as tasks:
        task = json.load(tasks)
        date = datetime.datetime.now()
        for x in task : 
            if x["id"] == task_id :
                x["name"] = task_value.name
                x["description"] = task_value.description
                x["status"] = task_value.status
                x["updatedAt"] = str(date)
                x["subTask"] = {
                    "subTaskname":task_value.subTask.subTaskname,
                    "description":task_value.subTask.description,
                }

                tasks.seek(0)
                json.dump(task, tasks, indent = 8)
                tasks.truncate()
                return JSONResponse(status_code=200, content={"message": "Task updated successfully"})
            else : 
                return JSONResponse(status_code=404, content={"message": "Invalid task id"})


@app.delete("/task/{task_id}")
async def delete_task(task_id : Annotated[int,Path(gt=0,description="Id must be an integer value")]):
    global task_data
    task_file = open(task_data, 'r+')
    tasks = json.load(task_file)
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            task_file.seek(0)
            json.dump(tasks, task_file, indent = 8)
            task_file.truncate()
            return JSONResponse(status_code=200, content={"message": "Task deleted successfully"})
        else : 
            return JSONResponse(status_code=404, content={"message": "Invalid task id"})
            
        


