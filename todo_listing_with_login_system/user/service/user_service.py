import sys
sys.path.append("/opt/lampp/htdocs/fast_api/todo_listing_with_login_system/")
import pb.user_pb2_grpc as user_pb2_grpc
import grpc
import pb.user_pb2 as user_pb2
from db.models import User
from db.db import SessionLocal
from .module import get_hashed_password,verify_password
from gateway.api.jwt.jwt import create_access_token
from pydantic import ValidationError
from db.schemas import RegisterUser

class UserBaseService (user_pb2_grpc.UserServiceServicer) :
    
    # Register new User
    def RegisterUser(self, request, context):
        user_data = RegisterUser(
            user_name=request.user_name,
            email=request.email,
            password=request.password
        )

        db = SessionLocal()
        user = db.query(User).filter(User.user_name == request.user_name).first()
        if user is None:
            user_data.password =get_hashed_password(request.password)
            new_user = User(**user_data.dict())
            db.add(new_user)
            db.commit()
            return user_pb2.RegisterUserResponse(message="User created successfully")
        else:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details('Username already exists!')
            return user_pb2.RegisterUserResponse()
            
    # Login User
    def LoginUser(self, request, context):
        db = SessionLocal()
        user = db.query(User).filter(User.user_name == request.user_name).first()

        if user is None :
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Incorrect email or password!')
        hashed_pass = user.password

        if not verify_password(request.password, hashed_pass):
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Invalid email or password!')

        access_token = create_access_token(user.email)
        return user_pb2.LoginUserResponse(access_token=access_token)
        
    # Get user by id(parent_id)
    def GetUser(self, request, context):
            db = SessionLocal()
            user = db.query(User).filter(User.id == request.parent_id).first()
            user_data = user_pb2.User(
                id=user.id,
                user_name =user.user_name,
                email=user.email,
            )
            return user_pb2.GetUserResponse(user = user_data)
    
    # Get user by Email
    def GetUserByEmail(self, request, context):
        db = SessionLocal()
        user = db.query(User).filter(User.email == request.email).first()
        user_data = user_pb2.User(
            id=user.id,
            user_name =user.user_name,
            email=user.email,
        )
        return user_pb2.GetUserResponse(user = user_data)