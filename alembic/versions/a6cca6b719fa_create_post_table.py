"""create post table

Revision ID: a6cca6b719fa
Revises: 
Create Date: 2022-01-04 17:14:15.637870

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6cca6b719fa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts",sa.Column('id',sa.Integer(), nullable=False, primary_key=True),
    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
