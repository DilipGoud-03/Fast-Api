from datetime import datetime,time,timedelta
from typing_extensions import Annotated
import uuid
from fastapi import FastAPI,Body,File,Path,Cookie,Header
from typing import Union

app = FastAPI()

@app.put("/item/{id}")
async def read_item(
    item_id :int,
    created_at  : Annotated[datetime,Body()],
    updated_at : Annotated[datetime,Body()],
    process_after : Annotated[timedelta,Body()],
    repead_at : Annotated[Union[time,None],Body()] = None
    ) : 
    start_process = created_at + process_after
    duratiton = updated_at - start_process

    return {
        "item_id":item_id,
        "created_at":created_at,
        "updated_at":updated_at,
        "start_process":start_process,
        "repead_at" :repead_at,
        "duration":duratiton
    }