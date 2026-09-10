"""add prediction credits

Revision ID: ac9012d5e311
Revises: 82adb4c927c7
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "ac9012d5e311"
down_revision: Union[str, Sequence[str], None] = "82adb4c927c7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("users", "password_hash", existing_type=sa.String(), nullable=True)
    op.add_column("users", sa.Column("auth_subject", sa.String(), nullable=True))
    op.add_column("users", sa.Column("prediction_credits", sa.Integer(), server_default="20", nullable=False))
    op.add_column("users", sa.Column("last_credit_refresh", sa.DateTime(timezone=True), nullable=True))
    op.add_column("users", sa.Column("subscription_type", sa.String(), server_default="free", nullable=False))
    op.add_column("users", sa.Column("subscription_status", sa.String(), server_default="active", nullable=False))
    op.create_index("ix_users_auth_subject", "users", ["auth_subject"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_users_auth_subject", table_name="users")
    op.drop_column("users", "subscription_status")
    op.drop_column("users", "subscription_type")
    op.drop_column("users", "last_credit_refresh")
    op.drop_column("users", "prediction_credits")
    op.drop_column("users", "auth_subject")
    op.alter_column("users", "password_hash", existing_type=sa.String(), nullable=False)
