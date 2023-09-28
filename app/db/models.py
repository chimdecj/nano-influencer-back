from typing import List
from app.db.database import Base
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, Integer, Text, DateTime
from sqlalchemy.orm import relationship


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
    
    
class Organization(Base):
    __tablename__ = "Organization"
    id = Column(Integer, primary_key=True, index=True)
    organization_name = Column(String(50))
    industry = Column(String(50))
    sub_industry = Column(String(50))
    instagram_profile = Column(String(50))
    facebook_profile = Column(String(50))
    tiktok_profile = Column(String(50))
    preffered_category = Column(String(50))
    offce_address = Column(String(50))
    phonenumber = Column(String(50))
    email = Column(String(50))
    
    campaigns = relationship("Campaign", back_populates="org")
    
    
class Campaign(Base):
    __tablename__ = "Campaign"
    id = Column(Integer, primary_key=True, index=True)
    campaign_status = Column(String(50))
    campaign_owner = Column(String(50))
    campaign_name = Column(String(50))
    campaign_type = Column(String(50))
    campaign_logo_id = Column(String(50))
    campaign_start_date_time = Column(DateTime())
    campaign_end_date_time = Column(DateTime())
    campaign_summary = Column(String(50))
    campaign_guidance = Column(String(50))
    campaign_photo = Column(String(50))
    campaign_word = Column(String(50))
    org_id = Column(Integer, ForeignKey("Organization.id"))
    
    org = relationship("Organization", back_populates="campaigns")












