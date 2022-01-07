"""add last few columns to posts table

Revision ID: b179f8f1e6f8
Revises: fbf4d7e7b5d1
Create Date: 2022-01-06 14:36:53.716699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b179f8f1e6f8'
down_revision = 'fbf4d7e7b5d1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default="TRUE"),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
