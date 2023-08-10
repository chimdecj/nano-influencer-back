from typing import List
from datetime import date
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    age: int
    # email: str
    
    class Config:
        orm_mode = True

class Answer(BaseModel):
    question_id: int
    alternative_id: int
    
    class Config:
        orm_mode = True


class UserAnswer(BaseModel):
    user_id: int
    answers: List[Answer]
    
    class Config:
        orm_mode = True