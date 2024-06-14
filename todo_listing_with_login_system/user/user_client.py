import grpc
from google.protobuf.json_format import MessageToDict
import pb.user_pb2 as user_pb2
import pb.user_pb2_grpc as user_pb2_grpc

class UserClient(object):
    def __init__(self):
        self.channel = grpc.insecure_channel("localhost:50051")
        self.stub = user_pb2_grpc.UserServiceStub(self.channel)

    def get_user(self,parent_id):
        response = self.stub.GetUser(user_pb2.GetUserRequest(parent_id = parent_id))
        print(response)
        return MessageToDict(
            response
        )