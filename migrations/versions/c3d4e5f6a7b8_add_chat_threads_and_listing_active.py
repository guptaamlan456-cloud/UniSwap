"""Add chat threads and listing active flag

Revision ID: c3d4e5f6a7b8
Revises: b7c8d9e0f1a2
Create Date: 2026-05-10 18:10:00.000000

"""

from alembic import op
import sqlalchemy as sa


revision = "c3d4e5f6a7b8"
down_revision = "b7c8d9e0f1a2"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    listing_cols = {col["name"] for col in inspector.get_columns("listings")}
    if "is_active" not in listing_cols:
        op.add_column("listings", sa.Column("is_active", sa.Boolean(), nullable=True))
    op.execute("UPDATE listings SET is_active = 1 WHERE is_active IS NULL")
    op.alter_column("listings", "is_active", existing_type=sa.Boolean(), nullable=False)

    existing_tables = set(inspector.get_table_names())
    if "chat_threads" not in existing_tables:
        op.create_table(
            "chat_threads",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("listing_id", sa.Integer(), nullable=False),
            sa.Column("seller_id", sa.Integer(), nullable=False),
            sa.Column("buyer_id", sa.Integer(), nullable=False),
            sa.Column("status", sa.String(length=20), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.Column("updated_at", sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(["buyer_id"], ["users.id"]),
            sa.ForeignKeyConstraint(["listing_id"], ["listings.id"]),
            sa.ForeignKeyConstraint(["seller_id"], ["users.id"]),
            sa.PrimaryKeyConstraint("id"),
        )

    message_cols = {col["name"] for col in inspector.get_columns("messages")}
    if "thread_id" not in message_cols:
        op.add_column("messages", sa.Column("thread_id", sa.Integer(), nullable=True))

    fk_names = {fk["name"] for fk in inspector.get_foreign_keys("messages") if fk.get("name")}
    if "fk_messages_thread_id_chat_threads" not in fk_names:
        op.create_foreign_key(
            "fk_messages_thread_id_chat_threads",
            "messages",
            "chat_threads",
            ["thread_id"],
            ["id"],
        )


def downgrade():
    op.drop_constraint("fk_messages_thread_id_chat_threads", "messages", type_="foreignkey")
    op.drop_column("messages", "thread_id")
    op.drop_table("chat_threads")
    op.drop_column("listings", "is_active")
