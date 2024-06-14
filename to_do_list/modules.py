from fastapi.responses import JSONResponse
import models

# create multiple todo taask
async def create_multiple_todo_task(todo_id, todo_tasks, db):
    todos_task_data = [todo_task.model_dump() for todo_task in todo_tasks]

    if not todo_id:
        return JSONResponse(status_code=400, content="Invalid todo id")
    else:
        if todos_task_data:
            for task_data in todos_task_data:
                task_data["todo_id"] = todo_id 
            db.bulk_insert_mappings(models.TodoTasks, todos_task_data)
            db.commit()
            return JSONResponse(content=todos_task_data)
        else:
            return JSONResponse(status_code=400, content="Something went wrong")
