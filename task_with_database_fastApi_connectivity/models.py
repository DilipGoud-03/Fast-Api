from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base,engine

Base.metadata.create_all(engine)

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    task_status = Column(Enum('Pendding', 'Completed', name='task_status'), default='Pendding')
    sub_tasks = relationship("SubTask", back_populates="parent",cascade="all,delete")


class SubTask(Base):
    __tablename__ = "sub_tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey('tasks.id')) 
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    parent = relationship('Task', back_populates='sub_tasks')
