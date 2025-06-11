"""add status field to InstrumentPost\n\nRevision ID: add_status_field\nRevises: c3305e59d32c\nCreate Date: 2025-06-10\n\n"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_status_field'
down_revision = 'c3305e59d32c'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('instrument_post', sa.Column('status', sa.String(length=20), nullable=False, server_default='available'))

def downgrade():
    op.drop_column('instrument_post', 'status')
