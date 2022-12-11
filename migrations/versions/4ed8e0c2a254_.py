"""empty message

Revision ID: 4ed8e0c2a254
Revises: 792d3aa21d7c
Create Date: 2022-12-11 17:24:04.433128

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ed8e0c2a254'
down_revision = '792d3aa21d7c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(length=200), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.drop_column('description')

    # ### end Alembic commands ###
