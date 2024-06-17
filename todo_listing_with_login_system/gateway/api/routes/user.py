from fastapi import APIRouter,Depends
from api.dependencies.grpc.user import UserClient
from ..db.schemas import RegisterUser,TokenSchema,UserOut
from fastapi.security import OAuth2PasswordRequestForm
from api.dependencies.dependency import get_current_user
from ..db.models import User

router = APIRouter()
user_client = UserClient()

@router.post("/register",status_code=201) 
def register_user(user : RegisterUser ):
    response = user_client.register(user=user)
    return response

@router.post("/login",response_model=TokenSchema)
def login_user (form_data: OAuth2PasswordRequestForm = Depends()):
    response = user_client.login(form_data)
    return response

@router.get("/user",status_code=201,response_model=UserOut) 
def get_user(owner: User = Depends(get_current_user)):
    return owner
