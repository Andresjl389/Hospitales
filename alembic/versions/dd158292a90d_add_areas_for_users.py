"""add areas for users

Revision ID: dd158292a90d
Revises: f1803253f80a
Create Date: 2025-09-30 10:41:02.255012

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd158292a90d'
down_revision: Union[str, Sequence[str], None] = 'f1803253f80a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
