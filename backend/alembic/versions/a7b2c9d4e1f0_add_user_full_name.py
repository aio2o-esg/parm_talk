"""add user full name

Revision ID: a7b2c9d4e1f0
Revises: 4583c5fccda3
Create Date: 2026-09-25
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a7b2c9d4e1f0"
down_revision: Union[str, None] = "4583c5fccda3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("full_name", sa.String(), nullable=True))
    op.execute("UPDATE users SET full_name = split_part(email, '@', 1) WHERE full_name IS NULL")
    op.alter_column("users", "full_name", nullable=False)


def downgrade() -> None:
    op.drop_column("users", "full_name")
