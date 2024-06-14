from fastapi import FastAPI,Path,Query
from pydantic import Field,BaseModel
from typing_extensions import Annotated
from fastapi.responses import JSONResponse
from typing import Union
import datetime
from connector import *


class Task(BaseModel) :
    name : Union[str,None] = Field(description="name must have at least 5 charaters",min_length=5,max_length=10)
    description : Union[str,None] = Field(description="Description must have at least 10 charaters",min_length=10,max_length=100)
    status : Union[str,None]= Field(default="Pandding", description="Status will be Pandding or Completed")

app = FastAPI()


@app.get("/task/{task_id}")
async def get_task(task_id : Annotated[int,Path(gt=0,description="Id must be an integer value")]):
    sql = "SELECT * FROM task WHERE id = %s"
    value = (task_id,)
    cursr.execute(sql,value)
    result = cursr.fetchone
    cursr.close()
    conn.close()
    if  result:

        return JSONResponse(status_code=200, content=result)

    else :
        return JSONResponse(status_code=404, content={"message": "Task id not found"})

@app.get("/filteredTask")
def get_filterd_task (q : Annotated[Union[str,None],Query(description="Filtere by status 'Pandding or Completed' and sort by task name",min_length=5,max_length=10)]) :
    sql = "SELECT * FROM task WHERE status = %s  OR name = %s"
    value = (q,q,)   
    cursr.execute(sql,value)
    result = cursr.fetchall

    if result :
        return result
    else : 
        return JSONResponse(status_code=404, content={"message": "Task data not found"})
 
@app.post("/createTask",response_model=Task)
async def create_new_task (task_value :Task) :

    date = str(datetime.datetime.now())

    sql = ("INSERT INTO task"
           "(name,description,status,created_at,update_at)"
           "VALUE(%s,%s,%s,%s,%s)")
    
    value =(
        task_value.name,
        task_value.description,
        task_value.status,
        date,
        date
    )
    cursr.execute(sql,value)
    conn.commit()
    conn.close()
    cursr.close()
    
    return value

@app.put("/updateTask/{task_id}")
async def update_task (task_id :Annotated[int,Path(gt=0,description="Id must be an integer value")],task_value : Task) :
    date = str(datetime.datetime.now())

    if task_id :
        sql = ("UPDATE task SET name = %s,description = %s,status = %s,update_at =%s WHERE id = %s")

        value =(
            task_value.name,
            task_value.description,
            task_value.status,
            date,
            task_id
        )
        cursr.execute(sql,value)
        conn.commit()
        conn.close()
        cursr.close()
           
        return JSONResponse(status_code=200, content={"message": "Task updated successfully"})
    else : 
        return JSONResponse(status_code=404, content={"message": "Invalid task id"})


@app.delete("/task/{task_id}")
async def delete_task(task_id : Annotated[int,Path(gt=0,description="Id must be an integer value")]):
        if task_id :
            sql = "DELETE FROM task WHERE id = %s "
            value = (task_id,)
            cursr.execute(sql,value)
            conn.commit()
            conn.close()
            cursr.close()
            return JSONResponse(status_code=200, content={"message": "Task deleted successfully"})
        else : 
            return JSONResponse(status_code=404, content={"message": "Invalid task id"})
            
