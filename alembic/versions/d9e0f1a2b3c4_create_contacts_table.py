"""create_contacts_table

Revision ID: d9e0f1a2b3c4
Revises: c8d9e0f1a2b3
Create Date: 2026-09-06 22:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9e0f1a2b3c4'
down_revision: Union[str, Sequence[str], None] = 'c8d9e0f1a2b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'contacts',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('client_id', sa.Integer(), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('subject', sa.String(length=255), nullable=True),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('status', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_contacts_client_id'), 'contacts', ['client_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_contacts_client_id'), table_name='contacts')
    op.drop_table('contacts')
