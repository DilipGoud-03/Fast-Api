import sys
sys.path.append("/opt/lampp/htdocs/fast_api/userContact/")
import pb.contact_pb2 as contact_pb2
from grpc import StatusCode
from grpc_interceptor.exceptions import GrpcException
import pb.contact_pb2_grpc as contact_pb2_grpc
from db import models
from db.db import SessionLocal
from user_MS.userClient import UserClient

class ContactBaseService (contact_pb2_grpc.ContactServiceServicer) :

# For create new user
    def CreateContact(self, request, context):
        db = SessionLocal()
        user = db.query(models.User).filter(models.User.id == request.user_id).first()
        if user :
            if user.email == request.email :
                raise GrpcException(  
                    details="THIS EMAIL IS SAME AS PARENT USER EMAIL !",  
                    status_code=StatusCode.ALREADY_EXISTS,  
                )
            else :
                email_check =[contact_email for contact_email in user.contacts if contact_email.email == request.email]
                if not email_check :
                    new_contact = models.Contact( user_id = request.user_id,first_name=request.first_name,last_name=request.last_name,email=request.email)
                    db.add(new_contact)
                    db.commit()
                    db.refresh(new_contact)
                    return contact_pb2.CreateContactResponse(message = "Contact add successful")
                else :
                    raise GrpcException(  
                        details="THIS EMAIL IS ALL READY EXIST !",  
                        status_code=StatusCode.ALREADY_EXISTS,  
                    )
        else :
            raise GrpcException(
                details="USER ID NOT FOUND !",  
                status_code=StatusCode.NOT_FOUND,  
            )

    # Get contacts with their user
    def GetContactListWithUser(self, request, context):
        user_client = UserClient()
        db = SessionLocal()
        contact_data = db.query(models.Contact).all()
        contacts_list =[]
        for contact in contact_data :
            # Calling userClient.py file
            user = user_client.user_by_contact(parent_id=contact.parent.id)
            user_data = user['user']
            contacts_list.append(contact_pb2.ContactWithUser(
                id = contact.id,
                first_name=contact.first_name,
                last_name=contact.last_name,
                email=contact.email,
                user = user_data
            ))
        return contact_pb2.ContactListRespectiveUserResponse(contacts = contacts_list)

    # Get only contact list
    def GetContactList(self, request, context):
        db = SessionLocal()
        contact_list = []
        contact_data = db.query(models.Contact).filter(models.Contact.user_id == request.user_id).all()
        for contacts in contact_data :
            contact_list.append(contact_pb2.Contact(
                id= contacts.id,
                first_name= contacts.first_name,
                last_name= contacts.last_name,
                email= contacts.email,
            ))
        return contact_pb2.ContactListResponse(contact = contact_list)
