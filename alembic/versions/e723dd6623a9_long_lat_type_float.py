"""long lat type float

Revision ID: e723dd6623a9
Revises: 9f879392463c
Create Date: 2022-10-19 22:17:07.583547

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e723dd6623a9'
down_revision = '9f879392463c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('greenhouse', 'longitude', type_=sa.Float())
    op.alter_column('greenhouse', 'latitude', type_=sa.Float())


def downgrade() -> None:
    op.alter_column('greenhouse', 'longitude', type_=sa.Integer())
    op.alter_column('greenhouse', 'latitude', type_=sa.Integer())
