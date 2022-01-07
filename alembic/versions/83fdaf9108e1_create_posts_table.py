"""create posts table

Revision ID: 83fdaf9108e1
Revises: 
Create Date: 2022-01-05 22:10:33.004727

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83fdaf9108e1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(),
     nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
