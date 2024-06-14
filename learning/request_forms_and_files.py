from fastapi import FastAPI,UploadFile,File,Form
from pydantic import BaseModel,EmailStr
from typing_extensions import Annotated
from typing import Union




app = FastAPI()


@app.post("/uploadFile/")
def create_file (
    file1 : Annotated[bytes,File()],
    file2 : Annotated[UploadFile,File()],
    token  :Annotated[str,Form()]
                ):
    return  {
        "file_size":len(file1),
        "content_type" : file2.content_type,
        "token" : token
            }