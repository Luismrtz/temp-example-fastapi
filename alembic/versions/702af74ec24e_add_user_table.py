"""add user table

Revision ID: 702af74ec24e
Revises: 7efa1cbb5457
Create Date: 2022-01-06 13:52:52.803533

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '702af74ec24e'
down_revision = '7efa1cbb5457'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                                server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
