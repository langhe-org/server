"""add irrigation

Revision ID: e0ccdf55c173
Revises: a57396427e37
Create Date: 2022-08-09 21:44:24.669605

"""
from alembic import op
import sqlalchemy as sa
import enum


# revision identifiers, used by Alembic.
revision = 'e0ccdf55c173'
down_revision = 'a57396427e37'
branch_labels = None
depends_on = None


class EnvironmentState(enum.Enum):
    Default = "Default"

class ControlMode(enum.Enum):
    automatic = "automatic"
    manual = "manual"



def upgrade() -> None:
    op.add_column('greenhouse_state', sa.Column('irrigation_mode', sa.Enum(ControlMode), nullable=True))
    op.execute("UPDATE greenhouse_state SET irrigation_mode = 'automatic'")
    op.alter_column('greenhouse_state', 'irrigation_mode', nullable=False)

    op.add_column('greenhouse_state', sa.Column('irrigation_state', sa.Enum(EnvironmentState), nullable=True))
    op.execute("UPDATE greenhouse_state SET irrigation_state = 'Default'")
    op.alter_column('greenhouse_state', 'irrigation_state', nullable=False)


def downgrade() -> None:
    op.drop_column('greenhouse_state', 'irrigation_mode')
    op.drop_column('greenhouse_state', 'irrigation_state')
