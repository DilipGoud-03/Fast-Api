from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .db import Base,engine


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True,autoincrement=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    contacts = relationship("Contact", back_populates="parent")

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True,autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    first_name = Column(String(255),nullable=False)
    last_name = Column(String(255),nullable=False)
    email = Column(String(255),nullable=False)
    parent = relationship("User", back_populates="contacts")

Base.metadata.create_all(engine)
