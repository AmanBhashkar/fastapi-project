"""add content column to posts table

Revision ID: 3ba44c0c52bc
Revises: a6cca6b719fa
Create Date: 2022-01-04 17:27:46.565276

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ba44c0c52bc'
down_revision = 'a6cca6b719fa'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
