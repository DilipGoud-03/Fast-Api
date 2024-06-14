from fastapi import FastAPI,Form,File,UploadFile
from typing_extensions import Annotated
from typing import List,Union

app = FastAPI()

# get swegger form with two field 
@app.post("/login")
def login_user(username : Annotated[str,Form()],password : Annotated[str,Form()]):
    return {"username":username , "password":password}

# read the file and get bype data
@app.post("/file")
def uploaded_file(file : Annotated[bytes,File()]) :
    return {"file size" : len(file)}

# upload file 
@app.post("/create_file")
def create_file(file : UploadFile):
    return {"file_name":file}

# upload multiple files 
@app.post("/multiplefiles/")
def add_multiple_file(file : List[UploadFile]):
    return {"files" : [files.filename for files in file ]}

# optional file data using Union

@app.post("/uploadfileUnion/")
async def create_upload_file(file: Annotated[Union[bytes, None], File()] = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file}
    

# optional file data using Union
@app.post("/uploadfileAnnotated/")
async def create_upload_file(file: Annotated[UploadFile, File(description="hello this is optional file with extra metadata")]):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}