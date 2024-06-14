from typing import Union
from fastapi import FastAPI,Cookie,Header
from typing_extensions import Annotated



app = FastAPI()

# Cookie
@app.get("/item/")
async def return_id(ads_id : Annotated[Union[str,None],Cookie()]=None):
    return{"ads_id":ads_id}


# Header 
@app.get("/user_id/")
async def return_user_id(user_id :Annotated[Union[str,None],Header()]= None):
    return {"user_id":user_id}
