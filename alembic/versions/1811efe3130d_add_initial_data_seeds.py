"""add initial data seeds

Revision ID: 1811efe3130d
Revises: dbf4fedc0bd9
Create Date: 2025-09-30 10:50:59.302914

"""
from datetime import datetime
from typing import Sequence, Union
import uuid

from alembic import op
import bcrypt
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1811efe3130d'
down_revision: Union[str, Sequence[str], None] = 'dbf4fedc0bd9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    conn = op.get_bind()

    # 1. Roles
    conn.execute(sa.text("""
        INSERT INTO roles (id, name) VALUES
        (:id1, 'Admin'),
        (:id2, 'User')
        ON CONFLICT (id) DO NOTHING
    """), {"id1": str(uuid.uuid4()), "id2": str(uuid.uuid4())})

    # 2. Statuses
    statuses = ["Pending", "In Progress", "Completed", "Expired"]
    for status in statuses:
        conn.execute(sa.text("INSERT INTO statuses (id, name) VALUES (:id, :name) ON CONFLICT DO NOTHING"),
                     {"id": str(uuid.uuid4()), "name": status})

    # 3. Departments
    departments = [
        "Oncología", "Cardiología", "Gastroenterología", "Farmacia",
        "Hemodinamia", "Rehabilitación", "Neumología", "Lab clínico",
        "Lab patologías", "Imágenes diagnósticas", "Salas de cirugía",
        "UCI 1", "UCI 2", "Odontología", "Habitación del sueño",
        "Consulta externa", "Hospitalización piso 2", "Hospitalización VIP",
        "Hospitalización piso 3", "Hospitalización piso 4", "Esterilización", "Administración", "Sin departamento"
    ]
    for dept in departments:
        conn.execute(sa.text("INSERT INTO areas (id, name) VALUES (:id, :name) ON CONFLICT DO NOTHING"),
                     {"id": str(uuid.uuid4()), "name": dept})

    # 4. Usuario Admin
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw("Admin123".encode("utf-8"), salt).decode("utf-8")

    conn.execute(sa.text("""
        INSERT INTO users (id, first_name, last_name, cedula, email, password, role_id, area_id, registered_at)
        VALUES (:id, :fn, :ln, :cedula, :email, :password, 
                (SELECT id FROM roles WHERE name = 'Admin'),
                (SELECT id FROM areas WHERE name = 'Administración'),
                :date)
        ON CONFLICT (email) DO NOTHING
    """), {
        "id": str(uuid.uuid4()),
        "fn": "Super",
        "ln": "Admin",
        "cedula": "00000000",
        "email": "admin@hospital.com",
        "password": hashed_password,
        "date": datetime.utcnow()
    })


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM users WHERE email='admin@hospital.com'"))
    conn.execute(sa.text("DELETE FROM roles WHERE name IN ('Admin','User')"))
    conn.execute(sa.text("DELETE FROM statuses"))
    conn.execute(sa.text("DELETE FROM areas"))
