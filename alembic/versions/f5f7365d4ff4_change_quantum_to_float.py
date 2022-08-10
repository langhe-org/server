"""Change quantum to float

Revision ID: f5f7365d4ff4
Revises: e0ccdf55c173
Create Date: 2022-08-10 06:47:09.585096

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5f7365d4ff4'
down_revision = 'e0ccdf55c173'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('greenhouse_state', 'quantum', type_=sa.Float)


def downgrade() -> None:
    op.alter_column('greenhouse_state', 'quantum', type_=sa.Integer)
