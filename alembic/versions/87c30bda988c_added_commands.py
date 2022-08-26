"""added commands

Revision ID: 87c30bda988c
Revises: d0f08d126143
Create Date: 2022-08-25 21:24:57.062499

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '87c30bda988c'
down_revision = 'd0f08d126143'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('commands',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('greenhouse_id', sa.Integer(), nullable=False),
        sa.Column('time', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('processed', sa.Boolean(), nullable=False),
        sa.Column('command', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.ForeignKeyConstraint(['greenhouse_id'], ['greenhouse.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_commands_time'), 'commands', ['time'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_commands_time'), table_name='commands')
    op.drop_table('commands')
    # ### end Alembic commands ###
