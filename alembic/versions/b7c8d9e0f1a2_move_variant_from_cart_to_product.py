"""set_product_variant_as_text

Revision ID: b7c8d9e0f1a2
Revises: 0382a417bb98
Create Date: 2026-09-05 07:45:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector


# revision identifiers, used by Alembic.
revision: str = 'b7c8d9e0f1a2'
down_revision: Union[str, Sequence[str], None] = '0382a417bb98'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)

    product_columns = [col['name'] for col in inspector.get_columns('products')]
    if 'varient' in product_columns and 'variant' not in product_columns:
        op.alter_column('products', 'varient', new_column_name='variant', existing_type=sa.String(200), type_=sa.Text(), nullable=True)
    elif 'variant' not in product_columns:
        op.add_column('products', sa.Column('variant', sa.Text(), nullable=True))
    else:
        op.alter_column('products', 'variant', existing_type=sa.String(200), type_=sa.Text(), nullable=True)


def downgrade() -> None:
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)

    product_columns = [col['name'] for col in inspector.get_columns('products')]
    if 'variant' in product_columns:
        op.alter_column('products', 'variant', existing_type=sa.Text(), type_=sa.String(200), nullable=True)


