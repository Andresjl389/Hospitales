"""add question types seeds

Revision ID: c44eb917d1ee
Revises: a948d98974b8
Create Date: 2025-10-07 17:50:49.687193

"""
from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c44eb917d1ee'
down_revision: Union[str, Sequence[str], None] = 'a948d98974b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    connection = op.get_bind()
    question_types = [
        {"id": str(uuid.uuid4()), "name": "Selección múltiple"},
        {"id": str(uuid.uuid4()), "name": "Múltiple respuesta"},
        {"id": str(uuid.uuid4()), "name": "Falso o verdadero"},
    ]

    for qt in question_types:
        connection.execute(
            sa.text("""
                INSERT INTO question_types (id, name)
                VALUES (:id, :name)
            """),
            qt
        )


def downgrade() -> None:
    connection = op.get_bind()
    connection.execute(
        sa.text("""
            DELETE FROM question_types
            WHERE name IN ('Selección múltiple', 'Múltiple respuesta', 'Falso o verdadero')
        """)
    )
