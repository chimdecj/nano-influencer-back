import bcrypt
import jwt 
from fastapi import Depends

from datetime import datetime, timedelta


def hash_password(password):
    hash = bcrypt.hashpw(password.encode("utf-8"), b'$2b$10$9Tw.yT.QYqVjHlpOPuN4Au')

    return hash.decode('utf-8')

def check_password(password, hashed_password): 
    return password == hashed_password
    # return bcrypt.checkpw(hashed_password.encode("utf-8"), password.encode("utf-8"))

def generate_access_token(data: dict, expires_delta: int = 3600):
    
    payload = {
        "sub": data["sub"],
        "exp": datetime.utcnow() + timedelta(minutes=30),
    }

    access_token = jwt.encode(data, "secret", algorithm="HS256")
    return access_token

