from services import contactService
import grpc
from concurrent import futures
import pb.contact_pb2_grpc as contact_pb2_grpc
from grpc_interceptor import ExceptionToStatusInterceptor

class ContactService(contactService.ContactBaseService) :
    pass

def serve () :
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),interceptors=interceptors)
    contact_pb2_grpc.add_ContactServiceServicer_to_server(ContactService(),server=server)
    server.add_insecure_port("[::]:50052")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__" :
    print ("Contact server running...")
    serve()


        