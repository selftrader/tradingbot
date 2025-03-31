"""add_token_expiry_to_broker_config

Revision ID: 05dd12f64da0
Revises: fba3585819bc
Create Date: 2025-03-29 23:28:34.578685

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '05dd12f64da0'
down_revision: Union[str, None] = 'fba3585819bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
