from typing import List, Optional
from datetime import datetime, date
from pydantic import BaseModel
from pydantic import Field

class CampaignImageBase(BaseModel):
    url: str
    campaign_id: int
    
    class Config:
        orm_mode = True

class CampaignImageCreate(CampaignImageBase):
    pass
    
class CampaignImage(CampaignImageBase):
    id: int

class SocialAccountBase(BaseModel):
    account_type:int = Field(description="0 bol Instagram")
    total_followers:int
    account_profile:str
    account_image:str
    last_updated:datetime
    
    class Config:
        orm_mode = True

class SocialAccountCreate(SocialAccountBase):
    pass

class SocialAccount(SocialAccountBase):
    inf_id:int


class InfluencerBase(BaseModel):
    phonenumber:Optional[str]
    email:Optional[str]
    first_name:Optional[str]
    last_name:Optional[str]
    dateofbirth:Optional[date]
    gender: Optional[int] = Field(description="0 bol eregtei, 1 bol emegtei")
    category: Optional[str]
    profession: Optional[str]
    work_position: Optional[str]
    work_name: Optional[str]
    work_address: Optional[str]
    family_count: Optional[str]
    home_address: Optional[str]
    bank: Optional[str]
    bankaccount: Optional[str]
    
    class Config:
        orm_mode = True

class InfluencerCreate(InfluencerBase):
    pass

class Influencer(InfluencerBase):
    id:int
    socialAccounts:List[SocialAccount] = []
    
        
class CampaignBase(BaseModel):
    status:Optional[int] = Field(description="#0-draft, 1-Submitted, 2-Active, 3-Finished")
    type:Optional[int] = Field(description="Product type #1-Ez Awareness")
    platform_type:Optional[int] = Field(description = "0- Instagram")
    title:Optional[str]
    start_date_time:Optional[datetime]
    end_date_time:Optional[datetime]
    created_date:Optional[datetime]
    updated_date:Optional[datetime]
    purpose:Optional[str]
    wording:Optional[str]
    guidance:Optional[str]
    owner_id:int
        
class CampaignCreate(CampaignBase):
    pass

class Campaign(CampaignBase):
    id:int
    org_id:int
    associated_influencers:List[Influencer] = []
    campaign_images:List[CampaignImage] = []
    
    class Config:
        orm_mode = True
        
class OrganizationBase(BaseModel):
    name:Optional[str] = None
    industry:Optional[str] = None
    sub_industry:Optional[str] = None
    instagram_profile:Optional[str] = None
    facebook_profile:Optional[str] = None
    tiktok_profile:Optional[str] = None
    preffered_category:Optional[str] = None
    offce_address:Optional[str] = None
    phonenumber:Optional[str] = None
    email:Optional[str] = None
        
        
class OrganizationCreate(OrganizationBase):
    pass

class Organization(OrganizationBase):
    id:int
    campaigns:List[Campaign] = []
    
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    password: str
    user_type: int
   
    class Config:
        orm_mode = True

class UserCreate(UserBase):
    pass

class User(UserBase):
    id:int
    org_id: Optional[int]
    inf_id: Optional[int]
    
class UserUpdate(UserBase):
    org_id:Optional[int] = None
    inf_id:Optional[int] = None
    
class UserReturn(BaseModel):
    id:int
    username: str
    user_type: int
    user_status: Optional[int]  = 0
    org_id:Optional[int] = None
    inf_id:Optional[int] = None
    
    class Config:
        orm_mode = True
        
class AssociatedInfluencer(BaseModel):
    campaign_id:int
    influencer_id:int
