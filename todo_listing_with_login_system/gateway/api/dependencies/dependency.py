from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..db.db import SessionLocal
from ..db.models import User
from jose import jwt
from pydantic import ValidationError
from ..db.schemas import TokenPayload, SystemUser

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)
def get_db() :
    try :
          db = SessionLocal()
          return db
    except :
         db.close()

async def get_current_user(token: str = Depends(reuseable_oauth),db : Session = Depends(get_db)):
    try:
        secret = "JWT_SECRET_KEY"
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user = db.query(User).filter(User.email == token_data.sub).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    else:
        return SystemUser(id=user.id,user_name=user.user_name,email=user.email,password=user.password)