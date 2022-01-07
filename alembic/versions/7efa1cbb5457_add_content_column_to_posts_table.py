"""add content column to posts table

Revision ID: 7efa1cbb5457
Revises: 83fdaf9108e1
Create Date: 2022-01-06 13:46:06.583059

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7efa1cbb5457'
down_revision = '83fdaf9108e1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
