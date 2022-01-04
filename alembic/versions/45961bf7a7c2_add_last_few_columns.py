"""add last few columns

Revision ID: 45961bf7a7c2
Revises: 26163d7ab068
Create Date: 2022-01-04 17:46:37.852786

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45961bf7a7c2'
down_revision = '26163d7ab068'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
