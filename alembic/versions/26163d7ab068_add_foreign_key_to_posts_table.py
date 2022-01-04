"""add foreign-key to posts table

Revision ID: 26163d7ab068
Revises: baf933f8b7c3
Create Date: 2022-01-04 17:34:48.012450

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26163d7ab068'
down_revision = 'baf933f8b7c3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("post_users_fk", source_table="posts", referent_table="users", local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass