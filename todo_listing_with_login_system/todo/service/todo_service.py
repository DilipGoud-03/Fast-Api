import sys
sys.path.append("/opt/lampp/htdocs/fast_api/todo_listing_with_auth/")
from grpc import StatusCode
import pb.todo_pb2_grpc as todo_pb2_grpc
import pb.todo_pb2 as todo_pb2
from grpc_interceptor.exceptions import GrpcException
from db import models
from db.db import SessionLocal
from comment_client import CommnetsClient
from user.user_client import UserClient

class TodoBaseService(todo_pb2_grpc.TodoServiceServicer):

    # Create new toto by
    def CreateTodo(self, request, context):
        db = SessionLocal()
        user = db.query(models.User).filter(models.User.id == request.user_id).first()
        if not user :
            raise GrpcException(
                details="User id not found !",  
                status_code=StatusCode.NOT_FOUND,  
            )
        else :
            new_todo = models.Todo( user_id = request.user_id,title=request.title,description=request.description)
            db.add(new_todo)
            db.commit()
            db.refresh(new_todo)
            return todo_pb2.CreateTodoResponse(message = "New Todo created successfuly")

    # Update todo item 
    def UpdateTodo(self, request, context):
        db = SessionLocal()
        todo = db.query(models.Todo).filter(models.Todo.id == request.todo_id).first()
        if not todo :
            raise GrpcException(
                details="TODO id not found !",  
                status_code=StatusCode.NOT_FOUND,  
            )
        else :
            if todo.user_id == request.user_id :
                todo.title = request.title
                todo.description = request.description
                db.commit()
                return todo_pb2.UpdateTodoResponse(message = "ToDo item updated")
            else :
                raise GrpcException(
                details="You can not update this TODO because, You are not owner of this TODO!",  
                status_code=StatusCode.NOT_FOUND,  
            )

    # Get all todo items or get by their id 
    def GetTodo(self, request, context):
        user_client = UserClient()
        commnet_client = CommnetsClient()
        db = SessionLocal()
        todo = db.query(models.Todo)
        if not todo :
            raise GrpcException(
                details="Does not have any TODO item in DB !",  
                status_code=StatusCode.NOT_FOUND,  
            )
        else :
            if request.todo_id :
                todo = db.query(models.Todo).filter(models.Todo.id == request.todo_id)
            todo_data = todo.all()
            if not todo_data :
                raise GrpcException(
                    details="TODO id not found !",  
                    status_code=StatusCode.NOT_FOUND,  
                )
            else :
                todo_list = []
                for result in todo_data :
                    user = user_client.get_user(parent_id=result.parent.id)
                    user_data = user["user"]
                    comments = commnet_client.get_comments(todo_id=result.id)
                    if comments :
                        comment_data = comments["comments"]
                        todo_list.append(todo_pb2.GetTodos(
                            id = result.id,
                            title = result.title,
                            description = result.description,
                            user = user_data,
                            comments = comment_data
                        ))
                    else :
                        todo_list.append(todo_pb2.GetTodos(
                            id = result.id,
                            title = result.title,
                            description = result.description,
                            user = user_data,
                            comments = []
                        ))
                return todo_pb2.GetTodoResponse(todos = todo_list)
    
    # Delete todo item
    def DeleteTodo(self, request, context):
        db  = SessionLocal()
        todo = db.query(models.Todo).filter(models.Todo.id == request.todo_id and models.Todo.user_id == request.user_id).first()
        if not todo :
            raise GrpcException(
                details="TODO id not found !",  
                status_code=StatusCode.NOT_FOUND, 
            )
        else :
            if todo.user_id == request.user_id :
                db.delete(todo)
                db.commit()
                return todo_pb2.DeleteTodoResponse(message="Todo item deleted")
            else :
                raise GrpcException(
                details="You can not delete this TODO because, You are not owner of this TODO!", 
                status_code=StatusCode.NOT_FOUND, 
            )

    # Create comment on any todo
    def CreateComment(self, request, context):
        db = SessionLocal()
        check_todo = db.query(models.Todo).filter(models.Todo.id == request.todo_id).first()
        check_user = db.query(models.User).filter(models.User.id == request.user_id).first()
        if check_todo and check_user :
            new_comment = models.Comment( user_id = request.user_id, todo_id = request.user_id,comment=request.comment)
            db.add(new_comment)
            db.commit()
            db.refresh(new_comment)
            return todo_pb2.CreateTodoResponse(message = "Comment created successfuly")
        else :
            if not check_user :
                raise GrpcException(
                    details="User id not found !",  
                    status_code=StatusCode.NOT_FOUND,  
                )
            else :
                raise GrpcException(
                    details="TODO id not found !",  
                    status_code=StatusCode.NOT_FOUND,  
                )
    
    # Get commnets 
    def GetComments(self, request, context):
        user_client = UserClient()
        db = SessionLocal()
        comments = db.query(models.Comment).filter(models.Comment.todo_id == request.todo_id).all()
        comment_list = []
        for result in comments :
            user = user_client.get_user(parent_id=result.parent.id)
            user_data = user["user"]
            comment_list.append(todo_pb2.Comment(
                id = result.id,
                comment = result.comment,
                user = user_data
            ))
        return todo_pb2.GetCommentsResponse(comments = comment_list)