"""init

Revision ID: ee9ed417ca86
Revises: 
Create Date: 2023-10-04 12:34:56.789012

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee9ed417ca86'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'User',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=True),
        sa.Column('password', sa.String(length=120), nullable=True),
        sa.Column('user_type', sa.Integer(), nullable=True),
        sa.Column('user_status', sa.Integer(), nullable=True),
        sa.Column('org_id', sa.Integer(), nullable=True),
        sa.Column('inf_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_User_id'), 'User', ['id'], unique=False)
    op.create_table(
        'Organization',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=True),
        sa.Column('industry', sa.String(length=200), nullable=True),
        sa.Column('sub_industry', sa.String(length=200), nullable=True),
        sa.Column('instagram_profile', sa.String(length=50), nullable=True),
        sa.Column('facebook_profile', sa.String(length=50), nullable=True),
        sa.Column('tiktok_profile', sa.String(length=50), nullable=True),
        sa.Column('preffered_category', sa.String(length=150), nullable=True),
        sa.Column('offce_address', sa.String(length=50), nullable=True),
        sa.Column('phonenumber', sa.String(length=50), nullable=True),
        sa.Column('email', sa.String(length=100), nullable=True),
        sa.Column('image_url', sa.String(length=200), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'Influencer',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('phonenumber', sa.String(length=50), nullable=True),
        sa.Column('email', sa.String(length=50), nullable=True),
        sa.Column('first_name', sa.String(length=50), nullable=True),
        sa.Column('last_name', sa.String(length=50), nullable=True),
        sa.Column('dateofbirth', sa.Date(), nullable=True),
        sa.Column('gender', sa.Integer(), nullable=True),
        sa.Column('category', sa.String(length=50), nullable=True),
        sa.Column('profession', sa.String(length=150), nullable=True),
        sa.Column('work_position', sa.String(length=150), nullable=True),
        sa.Column('work_name', sa.String(length=150), nullable=True),
        sa.Column('work_address', sa.String(length=500), nullable=True),
        sa.Column('family_count', sa.Integer(), nullable=True),
        sa.Column('home_address', sa.String(length=300), nullable=True),
        sa.Column('bank', sa.String(length=50), nullable=True),
        sa.Column('bankaccount', sa.String(length=50), nullable=True),
        sa.Column('image_url', sa.String(length=200), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'Campaign',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('status', sa.Integer(), nullable=True),
        sa.Column('type', sa.Integer(), nullable=True),
        sa.Column('platform_type', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(length=200), nullable=True),
        sa.Column('start_date_time', sa.DateTime(), nullable=True),
        sa.Column('end_date_time', sa.DateTime(), nullable=True),
        sa.Column('created_date', sa.DateTime(), nullable=True),
        sa.Column('updated_date', sa.DateTime(), nullable=True),
        sa.Column('purpose', sa.String(length=5000), nullable=True),
        sa.Column('wording', sa.String(length=500), nullable=True),
        sa.Column('guidance', sa.String(length=2500), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.Column('org_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Campaign_id'), 'Campaign', ['id'], unique=False)
    op.create_table(
        'SocialAccount',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('account_type', sa.Integer(), nullable=True),
        sa.Column('total_followers', sa.Integer(), nullable=True),
        sa.Column('account_profile', sa.String(length=150), nullable=True),
        sa.Column('account_image', sa.String(length=150), nullable=True),
        sa.Column('last_updated', sa.DateTime(), nullable=True),
        sa.Column('inf_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_SocialAccount_id'), 'SocialAccount', ['id'], unique=False)
    op.create_table(
        'Association_Influencers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('campaign_id', sa.Integer(), nullable=True),
        sa.Column('influencer_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Association_Influencers_id'), 'Association_Influencers', ['id'], unique=False)
    op.create_table(
        'CampaignImage',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('url', sa.String(length=500), nullable=True),
        sa.Column('campaign_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_CampaignImage_id'), 'CampaignImage', ['id'], unique=False)
    op.create_table(
        'CampaignStory',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('original_link', sa.String(length=500), nullable=True),
        sa.Column('created_date', sa.DateTime(), nullable=True),
        sa.Column('thumb_path', sa.String(length=500), nullable=True),
        sa.Column('story_path', sa.String(length=500), nullable=True),
        sa.Column('inf_id', sa.Integer(), nullable=True),
        sa.Column('campaign_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_CampaignStory_id'), 'CampaignStory', ['id'], unique=False)

    op.create_foreign_key('fk_user_org', 'User', 'Organization', ['org_id'], ['id'])
    op.create_foreign_key('fk_user_inf', 'User', 'Influencer', ['inf_id'], ['id'])
    op.create_foreign_key('fk_org_user', 'Organization', 'User', ['user_id'], ['id'])
    op.create_foreign_key('fk_inf_user', 'Influencer', 'User', ['user_id'], ['id'])
    op.create_foreign_key('fk_camp_user', 'Campaign', 'User', ['owner_id'], ['id'])
    op.create_foreign_key('fk_camp_org', 'Campaign', 'Organization', ['org_id'], ['id'])
    op.create_foreign_key('fk_sa_inf', 'SocialAccount', 'Influencer', ['inf_id'], ['id'])
    op.create_foreign_key('fk_assoc_camp', 'Association_Influencers', 'Campaign', ['campaign_id'], ['id'])
    op.create_foreign_key('fk_assoc_inf', 'Association_Influencers', 'Influencer', ['influencer_id'], ['id'])
    op.create_foreign_key('fk_campimg_camp', 'CampaignImage', 'Campaign', ['campaign_id'], ['id'])
    op.create_foreign_key('fk_campstory_inf', 'CampaignStory', 'Influencer', ['inf_id'], ['id'])
    op.create_foreign_key('fk_campstory_camp', 'CampaignStory', 'Campaign', ['campaign_id'], ['id'])


def downgrade() -> None:
    op.drop_table('CampaignStory')
    op.drop_table('CampaignImage')
    op.drop_table('Association_Influencers')
    op.drop_table('SocialAccount')
    op.drop_table('Campaign')
    op.drop_table('Influencer')
    op.drop_table('Organization')
    op.drop_table('User')