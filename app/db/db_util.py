from sqlalchemy.orm import Session
from . import models, schema

def check_influencer_in_campaign(db: Session, associated_influencer:schema.AssociatedInfluencer):
    campaign_influencer = db.query(models.CampaignInfluencers).filter(models.CampaignInfluencers.influencer_id ==associated_influencer.influencer_id, models.CampaignInfluencers.campaign_id==associated_influencer.campaign_id).all()
    if campaign_influencer:
        return True
    return False