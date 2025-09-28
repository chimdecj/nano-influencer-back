"""init

Revision ID: 3c820ed133ce
Revises: 
Create Date: 2023-09-30 10:17:10.409568

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c820ed133ce'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
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
        sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
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
        sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'User',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=True),
        sa.Column('password', sa.String(length=120), nullable=True),
        sa.Column('user_type', sa.Integer(), nullable=True),
        sa.Column('user_status', sa.Integer(), nullable=True),
        sa.Column('org_id', sa.Integer(), nullable=True),
        sa.Column('inf_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['inf_id'], ['Influencer.id'], ),
        sa.ForeignKeyConstraint(['org_id'], ['Organization.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_User_id'), 'User', ['id'], unique=False)
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
        sa.ForeignKeyConstraint(['org_id'], ['Organization.id'], ),
        sa.ForeignKeyConstraint(['owner_id'], ['User.id'], ),
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
        sa.ForeignKeyConstraint(['inf_id'], ['Influencer.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_SocialAccount_id'), 'SocialAccount', ['id'], unique=False)
    op.create_table(
        'Association_Influencers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('campaign_id', sa.Integer(), nullable=True),
        sa.Column('influencer_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['campaign_id'], ['Campaign.id'], ),
        sa.ForeignKeyConstraint(['influencer_id'], ['Influencer.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Association_Influencers_id'), 'Association_Influencers', ['id'], unique=False)
    op.create_table(
        'CampaignImage',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('url', sa.String(length=500), nullable=True),
        sa.Column('campaign_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['campaign_id'], ['Campaign.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_CampaignImage_id'), 'CampaignImage', ['id'], unique=False)
    op.create_table(
        'CampaignStory',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('original_link', sa.String(length=500), nullable=True),
        sa.Column('created_date', sa.DateTime(), nullable=True),
        sa.Column('thumb_path', sa.String(length=500), nullable=True),
        sa.Column('story_.path', sa.String(length=500), nullable=True),
        sa.Column('inf_id', sa.Integer(), nullable=True),
        sa.Column('campaign_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['campaign_id'], ['Campaign.id'], ),
        sa.ForeignKeyConstraint(['inf_id'], ['Influencer.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_CampaignStory_id'), 'CampaignStory', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_CampaignStory_id'), table_name='CampaignStory')
    op.drop_table('CampaignStory')
    op.drop_index(op.f('ix_CampaignImage_id'), table_name='CampaignImage')
    op.drop_table('CampaignImage')
    op.drop_index(op.f('ix_Association_Influencers_id'), table_name='Association_Influencers')
    op.drop_table('Association_Influencers')
    op.drop_index(op.f('ix_SocialAccount_id'), table_name='SocialAccount')
    op.drop_table('SocialAccount')
    op.drop_index(op.f('ix_Campaign_id'), table_name='Campaign')
    op.drop_table('Campaign')
    op.drop_index(op.f('ix_User_id'), table_name='User')
    op.drop_table('User')
    op.drop_table('Influencer')
    op.drop_table('Organization')