from fastapi import APIRouter,Depends
from api.dependencies.grpc.user import UserClient
from ..db.schemas import UserOut, RegisterUser,TokenSchema
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()
user_client = UserClient()

@router.post("/register") 
def register_user(user : RegisterUser ):
    response = user_client.register(user=user)
    return response

@router.post("/login",response_model=TokenSchema)
def login_user (form_data: OAuth2PasswordRequestForm = Depends()):
    response = user_client.login(form_data)
    return response
