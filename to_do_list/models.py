from database import Base,engine
from sqlalchemy import Column, Integer, String, Text,Boolean , ForeignKey
from sqlalchemy.orm import relationship



class ToDos(Base) :

    __tablename__ = "todos"
    
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String(255),nullable=False)
    description = Column(Text,nullable=True)
    completed  = Column(Boolean, default= False)
    todo_tasks = relationship("TodoTasks", back_populates="parent",cascade="delete")


class TodoTasks(Base):
    __tablename__ = "todo_tasks"
    id = Column(Integer, primary_key=True, index=True)
    todo_id = Column(Integer, ForeignKey('todos.id')) 
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False)
    parent = relationship('ToDos', back_populates='todo_tasks',cascade="delete")

Base.metadata.create_all(bind=engine)





