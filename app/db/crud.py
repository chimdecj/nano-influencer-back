from typing import List
from sqlalchemy.orm import Session
from datetime import date

from . import models, schema
import os


def get_org(db: Session, org_id: int):
    return db.query(models.Organization).filter(models.Organization.id == org_id).first()

def get_org_by_name(db: Session, name: str):
    return db.query(models.Organization).filter(models.Organization.name == name).first()


def get_orgs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Organization).offset(skip).limit(limit).all()

def create_orgs(db: Session, item: schema.OrganizationCreate):
    db_org = models.Organization(**item.dict())
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org

def update_org(db: Session, org_id: int, item: schema.OrganizationCreate):
    db_org = db.get(models.Organization, org_id)
    org_data = item.dict(exclude_unset=True)
    for key, value in org_data.items():
        setattr(db_org, key, value)
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org


def get_campaign(db: Session, campaign_id: int):
    """
    Get campaign by ID
    """
    return db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()


def get_campaign_by_name(db: Session, name: str, org_id:int):
    return db.query(models.Campaign).filter(models.Campaign.title == name, models.Campaign.org_id==org_id).first()


def get_campaigns_by_org_id(db: Session, org_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Campaign).filter(models.Campaign.org_id == org_id).order_by(models.Campaign.created_date.desc()).offset(skip).limit(limit).all()

def get_campaigns_by_status(db: Session, org_id: int, status:int, skip: int = 0, limit: int = 100):
    
    return db.query(models.Campaign).filter(models.Campaign.org_id == org_id, models.Campaign.status==status).order_by(models.Campaign.created_date.desc()).offset(skip).limit(limit).all()
 
def get_active_submitted_campaigns(db: Session, org_id: int, skip: int = 0, limit: int = 100):
    today = date.today()
    return db.query(models.Campaign).filter(models.Campaign.org_id == org_id, models.Campaign.status==1, models.Campaign.start_date_time <= today, models.Campaign.end_date_time >= today).order_by(models.Campaign.created_date.desc()).offset(skip).limit(limit).all()

def create_campaign(db: Session, item: schema.CampaignCreate, org_id:int):
    db_org = models.Campaign(**item.dict(), org_id=org_id)
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org

def add_influencer_to_campaign(db: Session, associated_influencer:schema.AssociatedInfluencer):
    campaign = get_campaign(db, campaign_id=associated_influencer.campaign_id)
    if campaign == None:
        return None;
    influencer = get_influencer(db=db, inf_id=associated_influencer.influencer_id)
    campaign.associated_influencers.append(influencer)
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign

def get_campaign_influencers(db:Session, campaign_id:int):
    campaign = get_campaign(db, campaign_id=campaign_id)
    if campaign == None:
        return None;
    return campaign.associated_influencers

def update_influencer_to_campaign(db: Session, campaign_id: int, influencer_ids:List[str]):
    campaign = get_campaign(db, campaign_id=campaign_id)
    if campaign == None:
        return None;
    db.query(models.CampaignInfluencers).filter(models.CampaignInfluencers.campaign_id == campaign_id).delete()
    for id in influencer_ids:
        influencer = get_influencer(db=db, inf_id=id)
        if influencer != None:
            campaign.associated_influencers.append(influencer)
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign


def remove_influencer_from_campaign(db: Session, associated_influencer:schema.AssociatedInfluencer):
    campaign = get_campaign(db, campaign_id=associated_influencer.campaign_id)
    if campaign == None:
        return None;
    influencer = get_influencer(db=db, inf_id=associated_influencer.influencer_id)
    campaign.associated_influencers.remove(influencer)
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign
    

def update_campaign(db: Session, item: schema.CampaignCreate, campaign_id:int):
    db_campaign = db.get(models.Campaign, campaign_id)
    campaign_data = item.dict(exclude_unset=True)
    for key, value in campaign_data.items():
        setattr(db_campaign, key, value)
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign

def submit_campaign(db: Session, campaign_id:int):
    db_campaign = db.get(models.Campaign, campaign_id)
    db_campaign.status = 1
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign

def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()

def get_user_by_name(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, item: schema.UserCreate):
    db_user = models.User(**item.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id:int, inf_id:int = None, org_id:int = None):
    db_user = db.get(models.User, user_id)
    if not db_user:
        return None
    if (inf_id != None):
        db_user.inf_id = inf_id
    if org_id != None:
        db_user.org_id = org_id
    db_user.user_status = 1
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_influencer(db: Session, inf_id: int):
    return db.query(models.Influencer).filter(models.Influencer.id == inf_id).first()

def get_influencer_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Influencer).offset(skip).limit(limit).all()

def get_influencer_campaigns(db: Session, influencer_id:int):
    db_campaigns =  db.query(models.Campaign)\
        .join(models.CampaignInfluencers)\
            .join(models.Influencer).filter(models.Influencer.id == influencer_id, models.Campaign.status != 0).order_by(models.Campaign.created_date.desc()).all()
    return db_campaigns

def get_influencer_campaigns_active_submitted(db: Session, influencer_id:int):
    today = date.today()
    db_campaigns =  db.query(models.Campaign)\
        .join(models.CampaignInfluencers)\
            .join(models.Influencer).filter(models.Influencer.id == influencer_id, models.Campaign.status == 1,  models.Campaign.start_date_time <= today, models.Campaign.end_date_time >= today).order_by(models.Campaign.created_date.desc()).all()
    return db_campaigns

def update_influencer(db: Session, inf_id:int,  item: schema.InfluencerCreate):
    db_influencer = db.get(models.Influencer, inf_id)
    inf_data = item.dict(exclude_unset=True)
    for key, value in inf_data.items():
        setattr(db_influencer, key, value)
    db.add(db_influencer)
    db.commit()
    db.refresh(db_influencer)
    return db_influencer


def create_influencer(db: Session, influencer_id:int, item: schema.InfluencerCreate):
    db_influencer = models.Influencer(**item.dict())
    db.add(db_influencer)
    db.commit()
    db.refresh(db_influencer)
    return db_influencer

def get_user_social_accounts(db: Session, inf_id: int):
    return db.query(models.SocialAccount).filter(models.SocialAccount.inf_id == inf_id).first()

def get_user_social_accounts_by_type(db: Session, inf_id: int, type: int):
    return db.query(models.SocialAccount).filter(models.SocialAccount.inf_id == inf_id, models.SocialAccount.account_type == type).first()

def create_social_account(db: Session, item: schema.SocialAccountCreate, inf_id: int):
    db_user = models.SocialAccount(**item.dict(), inf_id=inf_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_campaign_images(db: Session, campaign_id:int):
    db_campaign = db.get(models.Campaign, campaign_id)
    return db_campaign.campaign_images()

def delete_campaign_image(db: Session, image_id: int):
    db.query(models.CampaignImage).filter(models.CampaignImage.id == image_id).delete()
    db.commit()

def create_campaign_image(db: Session, url:str, campaign_id:int):
    db_user = models.CampaignImage(url=url, campaign_id=campaign_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

