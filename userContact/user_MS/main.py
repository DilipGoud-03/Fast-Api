import grpc
from concurrent import futures
from grpc_interceptor import ExceptionToStatusInterceptor
import pb.user_pb2_grpc as user_pb2_grpc
import services.userService as UserService

class UserServicer(UserService.UserBaseService):
    pass

def serve () :
    interceptor = [ExceptionToStatusInterceptor()]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),interceptors=interceptor)
    user_pb2_grpc.add_UserServiceServicer_to_server(UserServicer(),server=server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ =="__main__" :
    print("User server running...")
    serve()
