from typing import List
from app.db.database import Base
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Text


#https://blog.logrocket.com/server-side-rendering-with-fastapi-and-mysql/ enenii tutorial-r shaav

class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=False)
    age = Column(Integer)
    # email: str

class Answer(Base):
    __tablename__ = "Answer"
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer)
    alternative_id = Column(Integer)


class UserAnswer(Base):
    __tablename__ = "UserAnswer"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    # answers: List[Answer]
