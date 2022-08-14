"""Change sky_weather to str

Revision ID: 063c3b120949
Revises: cf2556777b23
Create Date: 2022-08-14 12:09:10.209266

"""
import enum
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '063c3b120949'
down_revision = 'cf2556777b23'
branch_labels = None
depends_on = None


class SkyWeather(enum.Enum):
    default = "default"


def upgrade() -> None:
    op.alter_column('greenhouse_state', 'weather_sky', type_=sa.String)



def downgrade() -> None:
    op.alter_column('greenhouse_state', 'weather_sky', type_=sa.Enum(SkyWeather))
