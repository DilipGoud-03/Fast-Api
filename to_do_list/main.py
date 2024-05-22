from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from database import SessionLocal
import models
import schema
from typing import List
from modules import create_multiple_todo_task

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
app = FastAPI()

# get all todo
@app.get('/todos/', response_model=List[schema.ToDo],tags=[schema.Tags.todo])
async def get_to_do(db :Session =Depends(get_db)):
    query = db.query(models.ToDos).all()
    if not query :
        return JSONResponse(status_code=400, content={"message":"Data not available"})
    else :
        return query

# get todo by id
@app.get('/todos/{id}',response_model=schema.ToDo,tags=[schema.Tags.todo])
async def get_to_do(id : int,db :Session =Depends(get_db)):
    query = db.query(models.ToDos).filter(models.ToDos.id == id).first()
    if not query :
        return JSONResponse(status_code=400, content={"message":"Data not available"})
    else :
        return query


# Create new todo
@app.post("/todos/",response_model=schema.ToDoCreate,tags=[schema.Tags.todo])
async def create_to_do(todoItem : schema.ToDoCreate,db : Session = Depends(get_db)):
    todo_data = models.ToDos(title = todoItem.title,description=todoItem.description,completed = todoItem.completed)
    db.add(todo_data)
    db.commit()
    await create_multiple_todo_task(todo_data.id,todoItem.todo_tasks,db)
    return todo_data
    

# Update todo
@app.put("/todos/{todo_id}",response_model=schema.ToDo,tags=[schema.Tags.todo])
async def update_to_do(todo_id : int,todoItem : schema.ToDoCreate,db:Session = Depends(get_db)) :
    todo_data = db.query(models.ToDos).filter(models.ToDos.id == todo_id).first()
    if not todo_data :
        return JSONResponse(status_code=400,content={"message" : "To Do id does not exist"})
    else :
        todo_data.title = todoItem.title
        todo_data.description = todoItem.description
        todo_data.completed = todoItem.completed
        db.commit()
        # db.refresh(todo_data)
        return todo_data

# Delete todo 
@app.delete("/todos/{todo_id}",response_model=schema.ToDoBase,tags=[schema.Tags.todo])
async def delete_todo(todo_id : int,db : Session= Depends(get_db)):
    todo_data = db.query(models.ToDos).filter(models.ToDos.id == todo_id).first()
    if not todo_data :
        return JSONResponse(status_code=400,content={"message":"To do Id does not exist in To do items"})
    else :
        db.delete(todo_data)
        db.commit()
        return JSONResponse (status_code=200 ,content={"message":"To do item deleted"})

# Get todo tasks by todo_id
@app.get("/todo_task/{todo_id}",tags=[schema.Tags.task])
async def get_todo_task(todo_id :int,db : Session = Depends(get_db)):
    todo_task_data = db.query(models.TodoTasks).filter(models.TodoTasks.todo_id == todo_id).all()
    if not todo_task_data :
        return JSONResponse(status_code=400,content={"message":"Data does not exist "})
    else :
        return todo_task_data


# Update tasks
@app.put("/todo_task/{todo_task_id}",response_model=schema.CreateToDoTask,tags=[schema.Tags.task])
async def update_todo_task(todo_task_id :int,task_data : schema.CreateToDoTask,db : Session = Depends(get_db)):
    todo_task_data = db.query(models.TodoTasks).filter(models.TodoTasks.id == todo_task_id).first()

    if not todo_task_data :
        return JSONResponse(status_code=400,content={"message" : "To Do id does not exist"})
    else :
        if task_data.completed == 1 or task_data.completed ==0:
            todo_task_data.name = task_data.name
            todo_task_data.description = task_data.description
            todo_task_data.completed = task_data.completed
            db.commit()
            db.refresh(todo_task_data)
            return todo_task_data
        else:
            return JSONResponse(status_code=400, content="Field 'completed' required only 'true' or 'false")

# Delete task by todo id and status
@app.delete("/todo_multiple_task/{todo_id}/{completed}",response_model=List[schema.TodoTaskBase],tags=[schema.Tags.task])
async def delete_multiple_todo_task(todo_id :int, completed :bool,db : Session = Depends(get_db)):

    task_data = db.query(models.TodoTasks).filter(models.TodoTasks.todo_id==todo_id and models.TodoTasks.completed == completed).all()
    if not task_data :
        return JSONResponse(status_code=400,content={"message":"Data does not exist "})
    else :
        for item in task_data :
            db.delete(item)
        db.commit()
        return task_data


@app.delete("/todo_task/{todo_task_id}",response_model=List[schema.TodoTaskBase],tags=[schema.Tags.task])
async def delete_todo_task(todo_task_id :int,db : Session = Depends(get_db)):

    task_data = db.query(models.TodoTasks).filter(models.TodoTasks.id==todo_task_id).first()
    if not task_data :
        return JSONResponse(status_code=400,content={"message":"Data does not exist "})
    else :
        for item in task_data :
            db.delete(item)
        db.commit()
        return task_data