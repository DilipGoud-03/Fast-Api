import grpc
from google.protobuf.json_format import MessageToDict
import api.pb.todo_pb2 as todo_pb2
import api.pb.todo_pb2_grpc as todo_pb2_grpc
from fastapi import HTTPException
from .error_mapping import grpc_to_http_status

class TodoClient(object):
    def __init__(self):
        self.channel = grpc.insecure_channel("localhost:50052")
        self.stub = todo_pb2_grpc.TodoServiceStub(self.channel)

    # Create new Todo item
    
    def create_new_todo(self,user_id,todo_data):
        try:
            response = self.stub.CreateTodo(todo_pb2.CreateTodoRequest(user_id=user_id,title=todo_data.title, description=todo_data.description))
            return MessageToDict(
                message=response
            )

        except grpc.RpcError as rpc_error:
            grpc_status_code = rpc_error.code()
            print(grpc_status_code)
            http_status_code = grpc_to_http_status.get(grpc_status_code)
            raise HTTPException(status_code=http_status_code, detail=rpc_error.details())

    # Get Todo items
    def get_todos(self,todo_id):
        try :
            responses  = self.stub.GetTodo(todo_pb2.GetTodoRequest(todo_id=todo_id))
            return MessageToDict(
                responses,
                always_print_fields_with_no_presence=True
            )
        except grpc.RpcError as rpc_error :
            grpc_status_code = rpc_error.code()
            print(grpc_status_code)
            http_status_code = grpc_to_http_status.get(grpc_status_code)
            raise HTTPException(status_code=http_status_code, detail=rpc_error.details())
    
    # Update Todo item
    def update_todo(self,user_id,todo_id,todo_data):
        try : 
            response = self.stub.UpdateTodo(todo_pb2.UpdateTodoRequest(user_id=user_id,todo_id=todo_id,title = todo_data.title,description = todo_data.description))
            return MessageToDict(
                response
            )
        except grpc.RpcError as rpc_error :
            grpc_status_code = rpc_error.code()
            print(grpc_status_code)
            http_status_code = grpc_to_http_status.get(grpc_status_code)
            raise HTTPException(status_code=http_status_code, detail=rpc_error.details())
        
    # Delete Todo item
    def delete_todo(self,user_id,todo_id):
        try :
            response = self.stub.DeleteTodo(todo_pb2.DeleteTodoRequest(user_id=user_id,todo_id=todo_id))
            return MessageToDict(
                response
            )
        except grpc.RpcError as rpc_error :
            grpc_status_code = rpc_error.code()
            print(grpc_status_code)
            http_status_code = grpc_to_http_status.get(grpc_status_code)
            raise HTTPException(status_code=http_status_code, detail=rpc_error.details())
    
    # Create new comment on todo
    def create_comment(self,user_id,todo_id,comment):
        try :
            response = self.stub.CreateComment(todo_pb2.CreateCommentRequest(user_id = user_id,todo_id=todo_id ,comment = comment))
            return MessageToDict(
                response
            )
        except grpc.RpcError as rpc_error :
            grpc_status_code = rpc_error.code()
            print(grpc_status_code)
            http_status_code = grpc_to_http_status.get(grpc_status_code)
            raise HTTPException(status_code=http_status_code, detail=rpc_error.details())
            
