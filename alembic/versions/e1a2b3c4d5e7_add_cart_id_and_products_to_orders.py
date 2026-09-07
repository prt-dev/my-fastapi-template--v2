"""add_cart_id_and_products_to_orders

Revision ID: e1a2b3c4d5e7
Revises: d9e0f1a2b3c4
Create Date: 2026-09-07 06:05:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1a2b3c4d5e7'
down_revision: Union[str, Sequence[str], None] = 'd9e0f1a2b3c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('orders', sa.Column('cart_id', sa.Integer(), nullable=True))
    op.add_column('orders', sa.Column('products', sa.Text(), nullable=True))
    op.create_index(op.f('ix_orders_cart_id'), 'orders', ['cart_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_orders_cart_id'), table_name='orders')
    op.drop_column('orders', 'products')
    op.drop_column('orders', 'cart_id')
