from fastapi import APIRouter,Query,Depends,Path
from ..db import schemas
from typing import Optional
from api.dependencies.grpc.todo import TodoClient
from api.dependencies.dependency import get_current_user
from ..db.models import User

router = APIRouter()
todo_client = TodoClient()

# Create Todo 
@router.post("/todo",status_code=201) 
def create_todo(todo : schemas.CreateTodo,owner: User = Depends(get_current_user)):
    response = todo_client.create_new_todo(user_id =owner.id,todo_data=todo)
    return response

# Get all todos
@router.get("/todos",status_code=200)
def get_todos (title :Optional[str] = Query(None, description="Filter by title"),owner: User = Depends(get_current_user)):
    response = todo_client.get_todos(user_id = owner.id,title = title)
    result = response["todos"]
    return result

# Get todo by their id 
@router.get("/todo/{todo_id}",status_code=200)
def get_todo(todo_id :int ,owner: User = Depends(get_current_user)):
    response = todo_client.get_todo(todo_id=todo_id,user_id = owner.id)
    result = response["todos"]
    return result

# Update Todo
@router.put("/todo/{todo_id}",status_code=201)
def update_todo(todo_id : int,todo : schemas.UpdateTodo,owner: User = Depends(get_current_user)) :
    response = todo_client.update_todo(user_id=owner.id,todo_id=todo_id,todo_data=todo)
    return response

# Delete Todo
@router.delete("/todo/{todo_id}",status_code=204)
def delete_todo(todo_id : int,owner: User = Depends(get_current_user)) :
    response = todo_client.delete_todo(user_id=owner.id,todo_id=todo_id)
    return response

# Create comment
@router.post("/comment/{todo_id}",status_code=201)
def create_comment(todo_id : int,comment : schemas.CreateComment,owner: User = Depends(get_current_user)):
    response = todo_client.create_comment(user_id=owner.id,todo_id=todo_id,comment=comment.comment)
    return response
