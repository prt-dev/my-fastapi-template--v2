"""add_products_to_carts

Revision ID: f2a3b4c5d6e8
Revises: e1a2b3c4d5e7
Create Date: 2026-09-07 06:36:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2a3b4c5d6e8'
down_revision: Union[str, Sequence[str], None] = 'e1a2b3c4d5e7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('carts', sa.Column('products', sa.Text(), nullable=True))
    op.alter_column('carts', 'product_id',
               existing_type=sa.Integer(),
               nullable=True)


def downgrade() -> None:
    op.alter_column('carts', 'product_id',
               existing_type=sa.Integer(),
               nullable=False)
    op.drop_column('carts', 'products')
