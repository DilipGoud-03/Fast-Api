import jwt
from typing import Union,Any
from datetime import datetime ,timedelta

def create_access_token(subject: Union[str, Any]) -> str:
    expires_delta = datetime.now() + timedelta(minutes=1)
    
    header = {  
        "alg": "HS256",  
        "typ": "JWT"  
        }  

    payload = {
        "sub": str(subject),
        "exp": expires_delta
        }
    secret = "JWT_SECRET_KEY"
    encoded_jwt = jwt.encode(payload,secret, algorithm="HS256",headers=header)
    return encoded_jwt