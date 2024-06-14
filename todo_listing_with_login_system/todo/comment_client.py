import grpc
from google.protobuf.json_format import MessageToDict
import pb.todo_pb2 as todo_pb2
import pb.todo_pb2_grpc as todo_pb2_grpc
from fastapi import HTTPException

class CommnetsClient(object):
    def __init__(self):
        self.channel = grpc.insecure_channel("localhost:50052")
        self.stub = todo_pb2_grpc.TodoServiceStub(self.channel)

    # Get Comments with user
    def get_comments(self,todo_id):
        try :
            responses  = self.stub.GetComments(todo_pb2.GetCommentsRequest(todo_id=todo_id))
            return MessageToDict(
                responses
            )
        except grpc.RpcError as rpc_error :
            http_status_code = 404
            raise HTTPException(status_code=http_status_code, detail=rpc_error.details())
