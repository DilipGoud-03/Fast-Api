import pb.user_pb2_grpc as user_pb2_grpc
import grpc
from concurrent import futures
from grpc_interceptor import ExceptionToStatusInterceptor
from service.user_service import UserBaseService

class UserService (UserBaseService) :
    pass

def serve () :
    interceptor = [ExceptionToStatusInterceptor()]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),interceptors=interceptor)
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(),server=server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ =="__main__" :
    print("User server running...")
    serve()