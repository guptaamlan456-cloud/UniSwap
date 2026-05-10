"""Add location to users and listings

Revision ID: a91b2c4d5e6f
Revises: 33e3827295f0
Create Date: 2026-05-10 14:10:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a91b2c4d5e6f"
down_revision = "33e3827295f0"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("users", sa.Column("location", sa.String(length=120), nullable=True))
    op.add_column("listings", sa.Column("location", sa.String(length=120), nullable=True))

    # Backfill existing rows to keep legacy data usable.
    op.execute("UPDATE users SET location = 'Unknown' WHERE location IS NULL")
    op.execute("UPDATE listings SET location = university WHERE location IS NULL")

    op.alter_column("listings", "location", existing_type=sa.String(length=120), nullable=False)


def downgrade():
    op.drop_column("listings", "location")
    op.drop_column("users", "location")
