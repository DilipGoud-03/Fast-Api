from fastapi import FastAPI, Path, Depends, Query,Body
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from typing import Union
from typing_extensions import Annotated
from database import SessionLocal
import models,schema


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/tasks/{task_id}")
async def get_task(task_id: Annotated[int,Path(gt=0,description="Id must be an integer value")], db: Session = Depends(get_db)):
    task_data = db.query(models.Task).filter(models.Task.id == task_id).first()
    sub_task_data = db.query(models.SubTask).filter(models.SubTask.task_id == task_id)

    if task_data is None or sub_task_data is None :
        return JSONResponse(status_code=404, content={"message": "Task data not found"})
    return {"task_data" : task_data , "sub_task_data" : sub_task_data.all() }

@app.get("/filteredTask/")
async def filtered_task(
    db: Session = Depends(get_db),
    status: Union[str,None] = Query(None,description="Filter by status and Only use 'Pendding' or 'Completed'",min_length=8,max_length=20),
    q: Union[str,None] = Query(None, description="Sort by 'name'"),
):
    query = db.query(models.Task)
    if status :
        if status == "Pendding" or status == "Completed" :
            query = query.filter(models.Task.task_status == status)
        else :        
            return JSONResponse(status_code=404, content={"message": "Please enter status like 'Pendding' or 'Completed'"})
    if q :
        query = query.filter(models.Task.name==q)
    result = query.all()
    if not result :
        return JSONResponse(status_code=404, content={"message": "data not found"})
    else :
        return result
    


@app.post("/createTask/")
async def create_task(task: schema.TaskCreate, db: Session = Depends(get_db)):
    # task_data = models.Task(name=task.name, description=task.description, task_status=task.task_status)
    task_data = models.Task(**task.model_dump())
    if task_data is None :
        return JSONResponse(status_code=404, content={"message": "Invalid task data"})
    else :
        if task.task_status =="Pendding" or task.task_status =="Completed" : 
            db.add(task_data)
            db.commit()
            db.refresh(task_data)
            return task_data
        else :
            return JSONResponse(status_code=404, content={"message": "Please enter status like 'Pendding' or 'Completed'"})

@app.put("/updateTask/{task_id}")
async def update_task(
    task_id :Annotated[int,
    Path(gt=0,description="Id must be an integer value")], 
    task_value: Annotated[schema.TaskCreate,Body(openapi_examples={
        "normal" : {
            "summary":"A valid data example",
            "description" :"this is example to enter correct data of your task",
            "value" :{
                "name" : "foods",
                "description":"you can describ you task",
                "task_status" : "Pendding"
            },
            
        },
        "invalid":{
            "summary" : "A invalid data example",
            "description":"This is example to if you enter invalid data",
            "value":{
                "name":"foo",
                "description" : "this is just well describe your description",
                "status" : "pendding"
            }
        }
    })], 
    db: Session = Depends(get_db)):
    task_data = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task_data is None :
        return JSONResponse(status_code=404, content={"message": "Task id not found"})
    else :
        if task_value.task_status =="Pendding" or task_value.task_status =="Pendding" : 

            task_data.name = task_value.name
            task_data.description = task_value.description
            task_data.task_status = task_value.task_status
            db.commit()
            db.refresh(task_data)
            return task_data
        
        return JSONResponse(status_code=404, content={"message": "Please enter status like 'Pendding' or 'Completed'"})
 

@app.delete("/deleteTask/{task_id}")
async def delete_task(task_id : Annotated[int,Path(gt=0,description="Id must be an integer value")], db: Session = Depends(get_db)):
    task_data = db.query(models.Task).filter(models.Task.id == task_id).first()

    if task_data  is None :
        return JSONResponse(status_code=404, content={"message": "Task id not found"})
    else :
        db.delete(task_data)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Task deleted"})


@app.post("/createSubTask/")
async def create_sub_tasks(sub_task : schema.SubTaskCreate,task_id : int,db :Session = Depends(get_db)):
    sub_task_data = models.SubTask(**sub_task.model_dump(),task_id=task_id)
    task_data = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task_data :
        db.add(sub_task_data)
        db.commit()
        db.refresh(sub_task_data)
        return sub_task_data
    else :
        return JSONResponse(status_code=404, content={"message": "Invalid task id"})



@app.put("/updateSubTask/{sub_task_id}")
async def update_sub_task(sub_task_id :Annotated[int,Path(gt=0,description="Id must be an integer value")], 
                          sub_task_value: Annotated[schema.SubTaskCreate,Body(examples=[
                            {
                                 "name": "Foo",
                                "description": "A very nice Item",
                            }
                            ])],
                            db: Session = Depends(get_db)):
    sub_task_data = db.query(models.SubTask).filter(models.SubTask.id == sub_task_id).first()
    if sub_task_data is None :
        return JSONResponse(status_code=404, content={"message": "Task id not found"})
    else :
        sub_task_data.name = sub_task_value.name
        sub_task_data.description = sub_task_value.description
        db.commit()
        db.refresh(sub_task_data)
        return sub_task_data
