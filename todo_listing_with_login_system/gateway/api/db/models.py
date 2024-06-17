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

Base.metadata.create_all(engine)