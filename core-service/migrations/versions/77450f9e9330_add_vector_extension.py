"""Add vector extension

Revision ID: 77450f9e9330
Revises: ea82989ed431
Create Date: 2026-01-24 16:33:37.669607

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "77450f9e9330"
down_revision: Union[str, Sequence[str], None] = "ea82989ed431"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.execute("ALTER TABLE inventory_items ADD COLUMN embedding vector(1024)")


def downgrade() -> None:
    op.execute("ALTER TABLE inventory_items DROP COLUMN embedding")
    op.execute("DROP EXTENSION vector")
