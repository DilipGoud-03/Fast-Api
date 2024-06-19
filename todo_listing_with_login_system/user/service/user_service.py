import pb.user_pb2_grpc as user_pb2_grpc
import grpc
import pb.user_pb2 as user_pb2
from db.models import User
from db.db import SessionLocal
from .module import get_hashed_password,verify_password
from db.schemas import user_schema
from jwt_token.jwt import create_access_token

def grpc_message_to_dict(message):
    return {field.name: getattr(message, field.name) for field in message.DESCRIPTOR.fields}
class UserBaseService (user_pb2_grpc.UserServiceServicer) :
    
    # Register new User
    def RegisterUser(self, request, context):
        db = SessionLocal()
        user = db.query(User).filter(User.user_name == request.user_name).first()
        if user is None:
            request.password = get_hashed_password(request.password)
            request_dict = grpc_message_to_dict(request)
            user_data = user_schema.load(request_dict, session=db)
            db.add(user_data)
            db.commit()
            return user_pb2.RegisterUserResponse(message="User created successfully")
        else:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details('Username already exists!')
            db.close()
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
                id= user.id,
                user_name=user.user_name,
                email=user.email
            )
            return user_pb2.GetUserResponse(user = user_data)
    
    # Get user by Email
    def GetUserByEmail(self, request, context):
        db = SessionLocal()
        user = db.query(User).filter(User.email == request.email).first()
        user_data = user_pb2.User(
            id= user.id, 
            user_name=user.user_name,
            email=user.email
        )
        return user_pb2.GetUserResponse(user = user_data)