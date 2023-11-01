"""empty message

Revision ID: 00ae8f6e0c95
Revises: 49f749ff4b13
Create Date: 2023-11-01 16:12:06.036699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00ae8f6e0c95'
down_revision = '49f749ff4b13'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('device_configurations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('device_configurations', schema=None) as batch_op:
        batch_op.drop_column('is_active')

    # ### end Alembic commands ###