"""Initial migration: User, Project, Task

Revision ID: 8a5a4d1d1791
Revises: ed86dcc3bd23
Create Date: 2025-11-10 22:10:16.037938

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a5a4d1d1791'
down_revision: Union[str, Sequence[str], None] = 'ed86dcc3bd23'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
