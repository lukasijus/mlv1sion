"""add google oauth columns

Revision ID: 6d6f6f4d13f0
Revises: 50176bb04c16
Create Date: 2025-02-15 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6d6f6f4d13f0"
down_revision: Union[str, Sequence[str], None] = "50176bb04c16"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users",
        "password_hash",
        existing_type=sa.String(),
        nullable=True,
    )
    op.add_column("users", sa.Column("google_id", sa.String(), nullable=True))
    op.create_unique_constraint("uq_users_google_id", "users", ["google_id"])


def downgrade() -> None:
    op.drop_constraint("uq_users_google_id", "users", type_="unique")
    op.drop_column("users", "google_id")
    op.alter_column(
        "users",
        "password_hash",
        existing_type=sa.String(),
        nullable=False,
    )
