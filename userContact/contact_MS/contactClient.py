import grpc
from google.protobuf.json_format import MessageToDict
import pb.contact_pb2 as contact_pb2
from pb.contact_pb2_grpc import ContactServiceStub

class ContactClient(object):
    def __init__(self):
        self.channel = grpc.insecure_channel("localhost:50052")
        self.stub = ContactServiceStub(self.channel)

# Get Contact list by user id
    def get_contacts (self ,user_id):
        response = self.stub.GetContactList(contact_pb2.ContactListRequest(user_id=user_id))
        return MessageToDict(
            response
        )
