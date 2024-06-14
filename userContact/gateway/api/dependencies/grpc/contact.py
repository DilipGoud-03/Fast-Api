from asyncio import start_unix_server
import grpc
from google.protobuf.json_format import MessageToDict
from sqlalchemy import true
import api.pb.contact_pb2 as contact_pb2
from api.pb.contact_pb2_grpc import ContactServiceStub
from fastapi import HTTPException
from .error_mapping import grpc_to_http_status

class ContactClient(object):
    def __init__(self):
        self.channel = grpc.insecure_channel("localhost:50052")
        self.stub = ContactServiceStub(self.channel)

# Get Contact list with thier users
    def get_contact_list(self):
        try:
            response = self.stub.GetContactListWithUser(contact_pb2.ContactListRespectiveUserRequest())
            return MessageToDict(response)
        
        except grpc.RpcError as rpc_error:
            grpc_status_code = rpc_error.code()
            http_status_code = grpc_to_http_status.get(grpc_status_code)
            raise HTTPException(status_code=http_status_code, detail=rpc_error.details())

# Create Contact by user_id
    def create_contact(self,user_id,contact):
        try:
            response = self.stub.CreateContact(contact_pb2.CreateContactRequest(user_id = user_id,first_name=contact.first_name,last_name=contact.last_name, email=contact.email))
            return MessageToDict(
                        response,
                        always_print_fields_with_no_presence=True
                    )
        except grpc.RpcError as rpc_error:
            grpc_status_code = rpc_error.code()
            print(grpc_status_code)
            http_status_code = grpc_to_http_status.get(grpc_status_code)
            raise HTTPException(status_code=http_status_code, detail=rpc_error.details())
