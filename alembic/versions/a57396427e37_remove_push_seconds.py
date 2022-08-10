"""remove push_seconds

Revision ID: a57396427e37
Revises: 
Create Date: 2022-08-09 07:25:32.681483

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a57396427e37'
down_revision = None
branch_labels = None
depends_on = None



def upgrade() -> None:
    op.drop_column('greenhouse_state', 'push_seconds')


def downgrade() -> None:
    op.add_column('greenhouse_state', sa.Column('push_seconds', sa.Integer, nullable=True))
    op.execute("UPDATE greenhouse_state SET push_seconds = 60")
    op.alter_column('greenhouse_state', 'push_seconds', nullable=False)
