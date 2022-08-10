"""Add Actuator.lights

Revision ID: 45695f3da903
Revises: f5f7365d4ff4
Create Date: 2022-08-10 07:06:27.611812

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45695f3da903'
down_revision = 'f5f7365d4ff4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('greenhouse_state', sa.Column('lights', sa.Boolean, nullable=True))
    op.execute("UPDATE greenhouse_state SET lights = true")
    op.alter_column('greenhouse_state', 'lights', nullable=False)


def downgrade() -> None:
    op.drop_column('greenhouse_state', 'lights')
