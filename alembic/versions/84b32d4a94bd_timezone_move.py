"""timezone move

Revision ID: 84b32d4a94bd
Revises: 45695f3da903
Create Date: 2022-08-10 07:15:28.304179

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84b32d4a94bd'
down_revision = '45695f3da903'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('greenhouse_state', 'dst')
    op.drop_column('greenhouse_state', 'timezone')
    op.add_column('greenhouse', sa.Column('timezone', sa.String, nullable=True))
    op.execute("UPDATE greenhouse SET timezone = 'America/New_York'")
    op.alter_column('greenhouse', 'timezone', nullable=False)


def downgrade() -> None:
    op.add_column('greenhouse_state', sa.Column('dst', sa.String, nullable=True))
    op.execute("UPDATE greenhouse_state SET dst = 0")
    op.alter_column('greenhouse_state', 'dst', nullable=False)

    op.add_column('greenhouse_state', sa.Column('timezone', sa.Float, nullable=True))
    op.execute("UPDATE greenhouse_state SET timezone = 0")
    op.alter_column('greenhouse_state', 'timezone', nullable=False)
