from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from ..db.schemas import TokenPayload, SystemUser
from .grpc.user import UserClient

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)

user_client = UserClient()

async def get_current_user(token: str = Depends(reuseable_oauth)):
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
    
    email =token_data.sub
    user = user_client.get_user_by_email(email).user
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    else:
        return SystemUser(id = user.id , user_name= user.user_name,email=user.email)