from sqlalchemy import Column, ForeignKey, Integer, String,Text
from sqlalchemy.orm import relationship
from .db import Base,engine

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True,autoincrement=True)
    user_name = Column(String(255),unique=True)
    email = Column(String(255), index=True)
    password = Column(String(255))
    todos = relationship("Todo", back_populates="parent")
    comments = relationship("Comment", back_populates="parent")

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True,autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    title = Column(String(255),nullable=False)
    description = Column(Text(255),nullable=False)
    parent = relationship("User", back_populates="todos")
    comments = relationship("Comment", back_populates="todo",cascade="all,delete")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True,autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    todo_id = Column(Integer, ForeignKey("todos.id"),nullable=False)
    comment = Column(Text(255),nullable=False)
    parent = relationship("User", back_populates="comments")
    todo = relationship("Todo", back_populates="comments")

Base.metadata.create_all(engine)