from fastapi import APIRouter, status, HTTPException,Depends
from ..db.schemas import UserOut,TokenSchema , RegisterUser
from sqlalchemy.orm import Session
from ..db.db import SessionLocal
from ..db.model import User
from fastapi.security import OAuth2PasswordRequestForm
from ..jwt.jwt import create_access_token
from ..dependencies.depp import get_current_user
from ..service.user_service import get_hashed_password,verify_password

router  = APIRouter()

def get_db() :
    try :
          db = SessionLocal()
          return db
    except :
         db.close()

@router.post('/signup', summary="Create new user", response_model=UserOut)
async def create_user(data: RegisterUser ,db : Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email and User.user_name ==data.user_name ).first()
    if user :
             raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This email already exist"
        )
    hash_pass =  get_hashed_password(data.password)
    new_user = User(user_name =data.user_name, email = data.email ,password = hash_pass)
    db.add(new_user)
    db.commit()
    return new_user



@router.post("/login", summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends() ,db : Session= Depends(get_db)):
    user = db.query(User).filter(User.user_name == form_data.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user.password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    return {
        "access_token": create_access_token(user.email),
    }

@router.get('/me', summary='Get details of currently logged in user', response_model=UserOut)
async def get_me(user: User = Depends(get_current_user)):
    return user