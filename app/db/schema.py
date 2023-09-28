from typing import List
from datetime import datetime
from pydantic import BaseModel
import pydantic


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
        
class CampaignBase(BaseModel):
    campaign_name:str
    campaign_status:str
    campaign_owner:str
    campaign_type:str
    campaign_logo_id:str
    campaign_start_date_time:datetime
    campaign_end_date_time:datetime
    campaign_summary:str
    campaign_guidance:str
    campaign_photo:str
    campaign_word:str
        
class CampaignCreate(CampaignBase):
    pass

class Campaign(CampaignBase):
    id:int
    org_id:int
    
    class Config:
        orm_mode = True
        
class OrganizationBase(BaseModel):
    organization_name:str
    industry:str
    sub_industry:str
    instagram_profile:str
    facebook_profile:str
    tiktok_profile:str
    preffered_category:str
    offce_address:str
    phonenumber:str
    email:str
        
        
class OrganizationCreate(OrganizationBase):
    pass

class Organization(OrganizationBase):
    id:int
    campaigns:List[Campaign] = []
    
    class Config:
        orm_mode = True



    