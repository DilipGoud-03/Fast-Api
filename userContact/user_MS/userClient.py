import grpc
from google.protobuf.json_format import MessageToDict
import pb.user_pb2 as user_pb2
from pb.user_pb2_grpc import UserServiceStub
from fastapi import HTTPException

class UserClient(object):
    def __init__(self):
        self.channel = grpc.insecure_channel("localhost:50051")
        self.stub = UserServiceStub(self.channel)

    # Get User by contact parent id
    def user_by_contact(self,parent_id):
        try:
            response = self.stub.GetUsers(user_pb2.UserByContactRequest(parent_id=parent_id))
            return MessageToDict(
                response
            )
        except grpc.RpcError as rpc_error:
            print(rpc_error.code())
            raise HTTPException(status_code=404, detail=rpc_error.details())
