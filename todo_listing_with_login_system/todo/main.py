import grpc
from concurrent import futures 
import pb.todo_pb2_grpc as todo_pb2_grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from service.todo_service import TodoBaseService

class TodoService (TodoBaseService) :
    pass

def serve () :
    interceptor = [ExceptionToStatusInterceptor()]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),interceptors=interceptor)
    todo_pb2_grpc.add_TodoServiceServicer_to_server(TodoService(),server=server)
    server.add_insecure_port("[::]:50052")
    server.start()
    server.wait_for_termination()

if __name__ =="__main__" :
    print("Todo server running...")
    serve()
