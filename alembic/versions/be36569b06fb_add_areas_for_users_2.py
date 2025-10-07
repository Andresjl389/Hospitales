"""add areas for users 2

Revision ID: be36569b06fb
Revises: dd158292a90d
Create Date: 2025-09-30 10:42:45.190121

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be36569b06fb'
down_revision: Union[str, Sequence[str], None] = 'dd158292a90d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
