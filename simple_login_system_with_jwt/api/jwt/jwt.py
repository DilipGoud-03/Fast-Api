from datetime import datetime, timedelta
from typing import Union, Any
import jwt

SECRET_KEY = "3c0e3dffa1c7ed86f9e21d1910109c082792dd3686832c5b93838b29b5c80680"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(subject: Union[str, Any]) -> str:

    expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    header = {  
        "alg": "HS256",  
        "typ": "JWT"  
        }  

    payload = {
        "sub": str(subject),
        "exp": expires_delta
        }
    encoded_jwt = jwt.encode(payload,SECRET_KEY, ALGORITHM ,headers=header)
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any]) -> str:

    expires_delta = datetime.utcnow() + timedelta(minutes=60*12*7)
    
    header = {  
        "alg": "HS256",  
        "typ": "JWT"  
        }
    
    payload = {
        "exp": expires_delta,
        "sub": str(subject)
        }
    
    
    encoded_jwt = jwt.encode(payload, SECRET_KEY, ALGORITHM,headers=header)
    return encoded_jwt