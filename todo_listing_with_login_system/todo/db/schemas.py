from .models import Comment,Todo
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema ,auto_field
class TodoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Todo
        load_instance = True 
        include_relationships = True
    user_id = auto_field()

todo_schema = TodoSchema()


class CommnetSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        load_instance = True
        include_relationships = True
    user_id = auto_field()
    todo_id = auto_field()

comment_schema = CommnetSchema()