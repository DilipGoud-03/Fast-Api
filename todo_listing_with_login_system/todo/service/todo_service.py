from grpc import StatusCode
import pb.todo_pb2_grpc as todo_pb2_grpc
import pb.todo_pb2 as todo_pb2
from grpc_interceptor.exceptions import GrpcException
from db import models
from db.db import SessionLocal
from comment_client import CommnetsClient
from user_client import UserClient
from pydantic import ValidationError
from db.schemas import CreateTodo,CreateComment


class TodoBaseService(todo_pb2_grpc.TodoServiceServicer):

    # Create new toto by
    def CreateTodo(self, request, context):
        todo_data = CreateTodo(**request.dict())
        db = SessionLocal()
        todo = db.query(models.Todo).filter(models.Todo.title == request.title,models.Todo.user_id == request.user_id).first()
        if todo :
            raise GrpcException(
                details="This TODO item is all ready exist",  
                status_code=StatusCode.ALREADY_EXISTS,
            )
        else :
            new_todo = models.Todo(**todo_data.dict())
            db.add(new_todo)
            db.commit()
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
                if request.title :
                    todo.title = request.title
                if request.description :
                    todo.description = request.description
                db.commit()
                return todo_pb2.UpdateTodoResponse(message = "ToDo item updated")
            else :
                raise GrpcException(
                details="You can not update this TODO because, You are not owner of this TODO!",  
                status_code=StatusCode.PERMISSION_DENIED,
            )

    # Get all todo items or get todo with sorting
    def GetTodo(self, request, context):
        user_client = UserClient()
        commnet_client = CommnetsClient()
        db =SessionLocal()
        todo = db.query(models.Todo).filter(models.Todo.user_id == request.user_id)
        if request.title:
            todo = todo.filter(models.Todo.title == request.title)
        
        todo_data = todo.all()
        
        if not todo_data:
            raise GrpcException(
                details="TODO item not found!",
                status_code=StatusCode.NOT_FOUND
            )
        
        todo_list = []
        for result in todo_data:
            user = user_client.get_user(parent_id=result.parent.id)
            user_data = user["user"] if user else None
            comments = commnet_client.get_comments(todo_id=result.id)
            comment_data = comments["comments"] if comments else []
            
            todo_list.append(todo_pb2.GetTodos(
                id=result.id,
                title=result.title,
                description=result.description,
                user=user_data,
                comments=comment_data
            ))
        
        return todo_pb2.GetTodoResponse(todos=todo_list)
    
    # Get Todo Item by their Id 
    def GetTodoById(self, request, context):
        user_client = UserClient()
        commnet_client = CommnetsClient()
        db = SessionLocal()
        todo = db.query(models.Todo).filter(
            models.Todo.id == request.todo_id,
            models.Todo.user_id == request.user_id
        ).first()
            
        if not todo:
            raise GrpcException(
                details="TODO id not found!",
                status_code=StatusCode.NOT_FOUND
            )

        user = user_client.get_user(parent_id=todo.parent.id)
        user_data = user["user"]
        comments = commnet_client.get_comments(todo_id=todo.id)
        comment_data = comments["comments"] if comments else []

        todo_list = [
            todo_pb2.GetTodos(
                id=todo.id,
                title=todo.title,
                description=todo.description,
                user=user_data,
                comments=comment_data
            )
        ]
        return todo_pb2.GetTodoResponse(todos=todo_list)

    # Delete todo item
    def DeleteTodo(self, request, context):
        db  = SessionLocal()
        todo = db.query(models.Todo).filter(models.Todo.id == request.todo_id ).first()
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
                status_code=StatusCode.PERMISSION_DENIED, 
            )

    # Create comment on any todo
    def CreateComment(self, request, context):
        
        comment_data = CreateComment(
            user_id=request.user_id,
            todo_id=request.todo_id,
            comment=request.comment,
        )
        db = SessionLocal()
        check_todo = db.query(models.Todo).filter(models.Todo.id == request.todo_id).first()
        if check_todo :
            new_comment = models.Comment(**comment_data.dict())
            db.add(new_comment)
            db.commit()
            return todo_pb2.CreateTodoResponse(message = "Comment created successfuly")
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