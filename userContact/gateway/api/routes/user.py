from fastapi import APIRouter
from ..db import schemas
from ..dependencies.grpc.user import UserClient

router = APIRouter()
user_client = UserClient()

@router.post("/user",status_code=201) 
def create_user(user_data : schemas.CreateUser) :
    response = user_client.create_user(user=user_data)
    return response

@router.get("/users",status_code=200)
def get_users() :
    responses = user_client.get_users_with_contacts()
    result = responses["users"]
    return result

