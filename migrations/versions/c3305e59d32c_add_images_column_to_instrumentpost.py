"""add images column to InstrumentPost

Revision ID: c3305e59d32c
Revises: ea239b077032
Create Date: 2025-06-05 19:10:26.922680

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c3305e59d32c'
down_revision = 'ea239b077032'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('instrument_post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('images', mysql.JSON(), nullable=True))
        batch_op.drop_column('image_filename')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('instrument_post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_filename', sa.VARCHAR(length=200), nullable=True))
        batch_op.drop_column('images')

    # ### end Alembic commands ###
