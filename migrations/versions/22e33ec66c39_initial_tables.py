"""Initial tables

Revision ID: 22e33ec66c39
Revises: 
Create Date: 2024-05-05 13:56:14.880629

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22e33ec66c39'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('weather',
    sa.Column('measurement_time', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('temperature', sa.Float(), nullable=False),
    sa.Column('wind_speed', sa.Float(), nullable=False),
    sa.Column('wind_direction', sa.Enum('NORTH', 'NORTH_EAST', 'EAST', 'SOUTH_EAST', 'SOUTH', 'WEST', 'NORTH_WEST', name='winddirection'), nullable=False),
    sa.Column('pressure', sa.Float(), nullable=False),
    sa.Column('rain', sa.Float(), nullable=False),
    sa.Column('showers', sa.Float(), nullable=False),
    sa.Column('snowfall', sa.Float(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_weather_id'), 'weather', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_weather_id'), table_name='weather')
    op.drop_table('weather')
    # ### end Alembic commands ###
