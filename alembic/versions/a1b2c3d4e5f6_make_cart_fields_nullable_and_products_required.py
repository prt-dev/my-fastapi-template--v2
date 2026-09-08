"""make_cart_fields_nullable_and_products_required

Revision ID: a1b2c3d4e5f6
Revises: f2a3b4c5d6e8
Create Date: 2026-09-08 14:31:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = 'f2a3b4c5d6e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('carts', 'products',
               existing_type=sa.Text(),
               nullable=False)
    op.alter_column('carts', 'product_id',
               existing_type=sa.Integer(),
               nullable=True)
    op.alter_column('carts', 'variant',
               existing_type=sa.String(length=255),
               nullable=True)
    op.alter_column('carts', 'quantity',
               existing_type=sa.Integer(),
               nullable=True,
               server_default=None)
    op.alter_column('carts', 'price',
               existing_type=sa.Float(),
               nullable=True,
               server_default=None)


def downgrade() -> None:
    op.alter_column('carts', 'price',
               existing_type=sa.Float(),
               nullable=False,
               server_default='0.0')
    op.alter_column('carts', 'quantity',
               existing_type=sa.Integer(),
               nullable=False,
               server_default='1')
    op.alter_column('carts', 'products',
               existing_type=sa.Text(),
               nullable=True)
