"""merge_heads

Revision ID: 0382a417bb98
Revises: 16fb4647d0cf, f1a2b3c4d5e6
Create Date: 2026-08-29 13:43:38.779832

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0382a417bb98'
down_revision: Union[str, Sequence[str], None] = ('16fb4647d0cf', 'f1a2b3c4d5e6')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
