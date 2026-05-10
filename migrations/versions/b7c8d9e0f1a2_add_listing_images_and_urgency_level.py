"""Add listing images and urgency level

Revision ID: b7c8d9e0f1a2
Revises: a91b2c4d5e6f
Create Date: 2026-05-10 15:20:00.000000

"""

from alembic import op
import sqlalchemy as sa


revision = "b7c8d9e0f1a2"
down_revision = "a91b2c4d5e6f"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("listings", sa.Column("image_urls", sa.Text(), nullable=True))
    op.add_column("listings", sa.Column("urgency_level", sa.String(length=20), nullable=True))


def downgrade():
    op.drop_column("listings", "urgency_level")
    op.drop_column("listings", "image_urls")
