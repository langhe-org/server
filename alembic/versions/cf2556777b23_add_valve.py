"""add valve

Revision ID: cf2556777b23
Revises: 45695f3da903
Create Date: 2022-08-12 07:24:49.077336

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON


# revision identifiers, used by Alembic.
revision = 'cf2556777b23'
down_revision = '45695f3da903'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('greenhouse_state', sa.Column('valves', JSON, nullable=True))
    op.execute("UPDATE greenhouse_state SET valves = '[false, false, false, false]'")
    op.alter_column('greenhouse_state', 'valves', nullable=False)


def downgrade() -> None:
    op.drop_column('greenhouse_state', 'valves')
