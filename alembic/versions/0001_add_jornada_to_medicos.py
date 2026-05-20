"""add jornada to medicos

Revision ID: 0001_add_jornada_to_medicos
Revises: 
Create Date: 2026-05-19
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

revision = '0001_add_jornada_to_medicos'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = inspect(bind)
    cols = [c['name'] for c in inspector.get_columns('medicos')]
    if 'jornada' not in cols:
        op.add_column('medicos', sa.Column('jornada', sa.String(length=20), nullable=True))


def downgrade():
    bind = op.get_bind()
    inspector = inspect(bind)
    cols = [c['name'] for c in inspector.get_columns('medicos')]
    if 'jornada' in cols:
        op.drop_column('medicos', 'jornada')
