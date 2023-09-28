from sqlalchemy.orm import Session

from . import models, schema


def get_org(db: Session, org_id: int):
    return db.query(models.Organization).filter(models.Organization.id == org_id).first()

def get_org_by_name(db: Session, name: str):
    return db.query(models.Organization).filter(models.Organization.organization_name == name).first()


def get_orgs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Organization).offset(skip).limit(limit).all()

def create_orgs(db: Session, item: schema.OrganizationCreate):
    db_org = models.Organization(**item.dict())
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org


def get_campaign(db: Session, campaign_id: int):
    return db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()

def get_campaign_by_name(db: Session, name: str, org_id:int):
    return db.query(models.Campaign).filter(models.Campaign.campaign_name == name, models.Campaign.org_id==org_id).first()


def get_campaigns_by_org_id(db: Session, org_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Campaign).filter(models.Campaign.org_id == org_id).offset(skip).limit(limit).all()

def create_campaign(db: Session, item: schema.CampaignCreate, org_id:int):
    db_org = models.Campaign(**item.dict(), org_id=org_id)
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org

