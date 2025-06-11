"""empty message

Revision ID: b946f6cbdc93
Revises: add_status_field, 2ed105feb893
Create Date: 2025-06-10 21:42:49.889127

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b946f6cbdc93'
down_revision = ('add_status_field', '2ed105feb893')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
