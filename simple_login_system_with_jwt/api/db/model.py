from sqlalchemy import Column, Integer, String
from .db import Base,engine

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True,autoincrement=True)
    user_name = Column(String(255), unique=True,index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))

Base.metadata.create_all(engine)