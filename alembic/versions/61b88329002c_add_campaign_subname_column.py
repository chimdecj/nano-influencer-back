"""add campaign subname column

Revision ID: 61b88329002c
Revises: 3c820ed133ce
Create Date: 2023-10-02 16:11:56.977003

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '61b88329002c'
down_revision: Union[str, None] = '3c820ed133ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
