import grpc
from google.protobuf.json_format import MessageToDict
import api.pb.user_pb2 as user_pb2
from api.pb.user_pb2_grpc import UserServiceStub
from fastapi import HTTPException
from .error_mapping import grpc_to_http_status

class UserClient(object):
    def __init__(self):
        self.channel = grpc.insecure_channel("localhost:50051")
        self.stub = UserServiceStub(self.channel)

# Create new user 
    def create_user(self,user):
        try:
            response = self.stub.CreateUser(user_pb2.CreateUserRequest(first_name=user.first_name,last_name=user.last_name, email=user.email,password=user.password))
            return MessageToDict(
                message=response
            )

        except grpc.RpcError as rpc_error:
            grpc_status_code = rpc_error.code()
            print(grpc_status_code)
            http_status_code = grpc_to_http_status.get(grpc_status_code)
            raise HTTPException(status_code=http_status_code, detail=rpc_error.details())

# Get User with their contact
    def get_users_with_contacts(self):
        try:
            responses = self.stub.ListUsersWithContacts(user_pb2.ListUsersWithContactsRequest())
            return MessageToDict(
                message=responses,
                always_print_fields_with_no_presence=True
            )
        except grpc.RpcError as rpc_error:
            grpc_status_code = rpc_error.code()
            print(grpc_status_code)
            http_status_code = grpc_to_http_status.get(grpc_status_code)
            raise HTTPException(status_code=http_status_code, detail=rpc_error.details())
        
