"""enum lowercase

Revision ID: 2bba06428b64
Revises: 063c3b120949
Create Date: 2022-08-15 07:15:33.462310

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2bba06428b64'
down_revision = '063c3b120949'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TYPE environmentstate RENAME VALUE 'Default' TO 'default'")
    op.execute("ALTER TYPE ipmstate RENAME VALUE 'Default' TO 'default'")
    # op.execute("ALTER TYPE irrigationstate RENAME VALUE 'Default' TO 'default'") # doesn't exist 🤷
    op.execute("ALTER TYPE lightningstate RENAME VALUE 'Default' TO 'default'")


def downgrade() -> None:
    op.execute("ALTER TYPE environmentstate RENAME VALUE 'default' TO 'Default'")
    op.execute("ALTER TYPE ipmstate RENAME VALUE 'default' TO 'Default'")
    # op.execute("ALTER TYPE irrigationstate RENAME VALUE 'default' TO 'Default'") # doesn't exist 🤷
    op.execute("ALTER TYPE lightningstate RENAME VALUE 'default' TO 'Default'")
