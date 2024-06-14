import grpc
from google.protobuf.json_format import MessageToDict
import api.pb.user_pb2 as user_pb2
import api.pb.user_pb2_grpc as user_pb2_grpc

from fastapi import HTTPException
from .error_mapping import grpc_to_http_status

class UserClient(object):
    def __init__(self):
        self.channel = grpc.insecure_channel("localhost:50051")
        self.stub = user_pb2_grpc.UserServiceStub(self.channel)

# Register new user 
    def register(self,user):
        try:
            response = self.stub.RegisterUser(user_pb2.RegisterUserRequest(user_name = user.user_name, email=user.email,password=user.password))
            return MessageToDict(
                message=response
            )
        
        except grpc.RpcError as rpc_error:
            grpc_status_code = rpc_error.code()
            print(grpc_status_code)
            http_status_code = grpc_to_http_status.get(grpc_status_code)
            raise HTTPException(status_code=http_status_code, detail=rpc_error.details())

    def login(self,user):
        try :
            response = self.stub.LoginUser(user_pb2.LoginUserRequest(user_name = user.username,password = user.password))            
            return response

        except grpc.RpcError as rpc_error:
            grpc_status_code = rpc_error.code()
            print(grpc_status_code)
            http_status_code = grpc_to_http_status.get(grpc_status_code)
            raise HTTPException(status_code=http_status_code, detail=rpc_error.details())
