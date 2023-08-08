from pydantic import BaseModel
from typing import List

class User(BaseModel):
    id: int
    name: str
    age: int
    # email: str

class Answer(BaseModel):
    question_id: int
    alternative_id: int


class UserAnswer(BaseModel):
    user_id: int
    answers: List[Answer]
