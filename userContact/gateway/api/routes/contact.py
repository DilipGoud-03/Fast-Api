from pickletools import read_uint1
from fastapi import APIRouter
from ..db import schemas
from ..dependencies.grpc.contact import ContactClient

router = APIRouter()
contact_client = ContactClient()

@router.post("/contact/{user_id}",status_code=201) 
def create_contact( user_id : int,contact_data : schemas.CreateContact) :
    response = contact_client.create_contact(user_id,contact_data)     
    return response

@router.get("/contacts",status_code=200)
def get_contact_with_users() :
    response = contact_client.get_contact_list()
    result = response["contacts"]
    return result