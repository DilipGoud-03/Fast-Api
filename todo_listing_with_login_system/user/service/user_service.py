import sys
sys.path.append("/opt/lampp/htdocs/fast_api/todo_listing_with_auth")
import pb.user_pb2_grpc as user_pb2_grpc
import pb.user_pb2 as user_pb2
from db.models import User
from db.db import SessionLocal
from grpc_interceptor.exceptions import GrpcException
from grpc import StatusCode
from .module import get_hashed_password,verify_password
from gateway.api.jwt.jwt import create_access_token

class UserBaseService (user_pb2_grpc.UserServiceServicer) :
    # Register new User
    def RegisterUser(self, request, context):
        db = SessionLocal()
        user = db.query(User).filter(User.email == request.email).first()
        if user is None:
            hashed_password= get_hashed_password(request.password)
            new_user = User(user_name = request.user_name,email=request.email,password=hashed_password)
            db.add(new_user)
            db.commit()
            return user_pb2.RegisterUserResponse(message="User created successfuly")
        else :
            raise GrpcException(
                    details="This email is all ready exist !",  
                    status_code=StatusCode.ALREADY_EXISTS,  
                )
    def LoginUser(self, request, context):
        db = SessionLocal()
        user = db.query(User).filter(User.user_name == request.user_name).first()
        if user is None :
               raise GrpcException(
                    detail="Incorrect email or password",
                    status_code=StatusCode.NOT_FOUND,
                )
        hashed_pass = user.password
        if not verify_password(request.password, hashed_pass):
            raise GrpcException(
                status_code=StatusCode.NOT_FOUND,
                detail="Incorrect email or password"
            )
        access_token = create_access_token(user.email)
        return user_pb2.LoginUserResponse(access_token=access_token)
        
          
    def GetUser(self, request, context):
            db = SessionLocal()
            user = db.query(User).filter(User.id == request.parent_id).first()
            user_data = user_pb2.User(
            id=user.id,
            user_name =user.user_name,
            email=user.email,)
            return user_pb2.GetUserResponse(user = user_data)
    