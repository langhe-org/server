"""removed states

Revision ID: 458e919b974d
Revises: e723dd6623a9
Create Date: 2022-10-19 22:29:50.742767

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '458e919b974d'
down_revision = 'e723dd6623a9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('greenhouse_state', 'environment_state')
    op.drop_column('greenhouse_state', 'lighting_state')
    op.drop_column('greenhouse_state', 'irrigation_state')
    op.drop_column('greenhouse_state', 'ipm_state')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('greenhouse_state', sa.Column('ipm_state', postgresql.ENUM('default', name='ipmstate'), autoincrement=False, nullable=False))
    op.add_column('greenhouse_state', sa.Column('irrigation_state', postgresql.ENUM('default', name='irrigationstate'), autoincrement=False, nullable=False))
    op.add_column('greenhouse_state', sa.Column('lighting_state', postgresql.ENUM('default', name='lightningstate'), autoincrement=False, nullable=False))
    op.add_column('greenhouse_state', sa.Column('environment_state', postgresql.ENUM('default', name='environmentstate'), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
