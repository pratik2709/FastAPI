"""create intial migration for device configuration service

Revision ID: e17fbca32525
Revises: 
Create Date: 2023-11-01 10:10:51.436231

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c096503827ae'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('device_configurations',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('device_id', sa.String(length=255), nullable=False),
                    sa.Column('app_config_uri', sa.String(length=512), nullable=False),
                    sa.Column('depth_config_uri', sa.String(length=512), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
                    sa.Column('created', sa.DateTime(), nullable=False),
                    sa.Column('updated', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('device_id')
                    )
    with op.batch_alter_table('device_configurations', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_device_configurations_created'), ['created'], unique=False)


def downgrade():
    with op.batch_alter_table('device_configurations', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_device_configurations_created'))

    op.drop_table('device_configurations')
