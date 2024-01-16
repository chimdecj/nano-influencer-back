from typing import List
from app.db.database import Base
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, Integer, Text, DateTime, Date
from sqlalchemy.orm import relationship


#https://blog.logrocket.com/server-side-rendering-with-fastapi-and-mysql/ enenii tutorial-r shaav

class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    password = Column(String(120))
    user_type = Column(Integer) #0-Org 1-Inf
    user_status = Column(Integer, default=0) #0-Org 1-Inf
    org_id = Column(Integer, ForeignKey("Organization.id"))
    inf_id = Column(Integer, ForeignKey("Influencer.id"))

    
class Influencer(Base):
    __tablename__ = "Influencer"
    id = Column(Integer, primary_key=True, index=True)
    phonenumber = Column(String(50))
    email = Column(String(50))
    first_name = Column(String(50))
    last_name = Column(String(50))
    dateofbirth = Column(Date())
    gender = Column(Integer) #0-er 1-em
    category = Column(String(50))
    profession = Column(String(150))
    work_position = Column(String(150))
    work_name = Column(String(150))
    work_address = Column(String(500))
    family_count = Column(Integer)
    home_address = Column(String(300))
    bank = Column(String(50))
    bankaccount = Column(String(50))
    image_url = Column(String(200))
    user_id = Column(Integer, ForeignKey("User.id"))
    socialAccounts = relationship("SocialAccount", back_populates="inf")
    
class SocialAccount(Base):
    __tablename__ = "SocialAccount"
    id = Column(Integer, primary_key=True, index=True)
    account_type = Column(Integer) #0-Instagram
    total_followers = Column(Integer)
    account_profile = Column(String(150))
    account_image = Column(String(150))
    last_updated = Column(DateTime())
    inf_id = Column(Integer, ForeignKey("Influencer.id"))
    inf = relationship("Influencer", back_populates="socialAccounts")

    
class Organization(Base):
    __tablename__ = "Organization"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150))
    industry = Column(String(200))
    sub_industry = Column(String(200))
    instagram_profile = Column(String(50))
    facebook_profile = Column(String(50))
    tiktok_profile = Column(String(50))
    preffered_category = Column(String(150))
    offce_address = Column(String(50))
    phonenumber = Column(String(50))
    email = Column(String(100))
    image_url = Column(String(200))
    
    user_id =  Column(Integer, ForeignKey("User.id"))
    
    campaigns = relationship("Campaign", back_populates="org")
    

class CampaignInfluencers(Base):
    __tablename__ = "Association_Influencers"
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("Campaign.id"))
    influencer_id = Column(Integer, ForeignKey("Influencer.id"))


class CampaignImage(Base):
    __tablename__ = "CampaignImage"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(500))
    campaign_id = Column(Integer, ForeignKey("Campaign.id"))
    campaign = relationship("Campaign", back_populates="campaign_images")
    
class CampaignStory(Base):
    __tablename__ = "CampaignStory"
    id = Column(Integer, primary_key=True, index=True)
    original_link =  Column(String(500))
    created_date = Column(DateTime())
    thumb_path = Column(String(500))
    story_path = Column(String(500))
    inf_id = Column(Integer, ForeignKey("Influencer.id"))
    campaign_id = Column(Integer, ForeignKey("Campaign.id"))
    campaign = relationship("Campaign", back_populates="campaign_stories")

class Campaign(Base):
    __tablename__ = "Campaign"
    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer) #0-draft, 1-Submitted, 2-Active, 3-Finished
    type = Column(Integer) #1-Ez Awareness
    platform_type = Column(Integer) #0-Instagram
    title = Column(String(200))
    start_date_time = Column(DateTime())
    end_date_time = Column(DateTime())
    created_date = Column(DateTime())
    updated_date = Column(DateTime())
    purpose = Column(String(5000))
    wording = Column(String(500))
    guidance = Column(String(2500))
    
    owner_id = Column(Integer, ForeignKey("User.id"))
    org_id = Column(Integer, ForeignKey("Organization.id"))
    org = relationship("Organization", back_populates="campaigns")
    associated_influencers = relationship('Influencer', secondary="Association_Influencers", backref='Campaigns')
    campaign_images = relationship('CampaignImage', back_populates="campaign")
    campaign_stories = relationship('CampaignStory', back_populates="campaign")
