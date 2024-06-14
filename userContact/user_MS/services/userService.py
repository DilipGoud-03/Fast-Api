import sys
sys.path.append("/opt/lampp/htdocs/fast_api/userContact")
import pb.user_pb2 as user_pb2
import pb.user_pb2_grpc as user_pb2_grpc
from db.models import User
from grpc import StatusCode
from grpc_interceptor.exceptions import GrpcException
from db.db import SessionLocal
from contact_MS.contactClient import ContactClient

contactClient = ContactClient()
class UserBaseService(user_pb2_grpc.UserServiceServicer):

    def CreateUser(self, request, context):
        db = SessionLocal()
        check_email = db.query(User).filter(User.email == request.email).first()
        if check_email is None:
            new_user = User(first_name=request.first_name,last_name=request.last_name,email=request.email,password=request.password)
            db.add(new_user)
            db.commit()
            return user_pb2.CreateUserResponse(message="User created successfuly")
        else :
            raise GrpcException(
                details="THIS EMAIL IS ALL READY EXIST !",  
                status_code=StatusCode.ALREADY_EXISTS,  
            )
        
    def ListUsersWithContacts(self, request, context):
        db = SessionLocal()
        users = db.query(User).all()
        if users :
            users_list = []
            for user in users:
                # Calling contactClient.py file
                contacts= contactClient.get_contacts(user.id)
                if contacts :
                    contacts_data = contacts['contact']
                    users_list.append(user_pb2.UserWithContacts(
                        id=user.id,
                        first_name=user.first_name,
                        last_name=user.last_name,
                        email=user.email,
                        contacts = contacts_data,
                    ))
                else :
                    users_list.append(user_pb2.UserWithContacts(
                    id=user.id,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    email=user.email,
                    contacts = [],
                ))
            return user_pb2.ListUsersWithContactsResponse(users = users_list)

# Get user by Parent id
    def GetUsers(self,request,context):
        db = SessionLocal()
        user = db.query(User).filter(User.id == request.parent_id).first()
        user_data = user_pb2.User(
           id=user.id,
           first_name=user.first_name,
           last_name=user.last_name,
           email=user.email,)
        return user_pb2.UserByContactResponse(user = user_data)