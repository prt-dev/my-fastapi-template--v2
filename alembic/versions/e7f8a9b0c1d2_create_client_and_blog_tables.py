"""create_client_and_blog_tables

Revision ID: e7f8a9b0c1d2
Revises: 94676986b6ec
Create Date: 2026-08-20 19:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e7f8a9b0c1d2'
down_revision: Union[str, Sequence[str], None] = '94676986b6ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### Create clients table ###
    op.create_table(
        'clients',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('website_name', sa.String(length=255), nullable=True),
        sa.Column('website_url', sa.String(length=500), nullable=True),
        sa.Column('domain', sa.String(length=255), nullable=True),
        sa.Column('logo', sa.String(length=500), nullable=True),
        sa.Column('default_meta_title', sa.String(length=255), nullable=True),
        sa.Column('default_meta_description', sa.Text(), nullable=True),
        sa.Column('status', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_clients_domain'), 'clients', ['domain'], unique=True)

    # ### Create blogs table ###
    op.create_table(
        'blogs',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('client_id', sa.Integer(), nullable=True),
        sa.Column('author_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('slug', sa.String(length=255), nullable=False),
        sa.Column('excerpt', sa.Text(), nullable=True),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('featured_image', sa.String(length=500), nullable=True),
        sa.Column('status', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('published_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('meta_title', sa.String(length=255), nullable=True),
        sa.Column('meta_description', sa.Text(), nullable=True),
        sa.Column('canonical_url', sa.String(length=500), nullable=True),
        sa.Column('og_title', sa.String(length=255), nullable=True),
        sa.Column('og_description', sa.Text(), nullable=True),
        sa.Column('og_image', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_blogs_slug'), 'blogs', ['slug'], unique=True)
    op.create_index(op.f('ix_blogs_client_id'), 'blogs', ['client_id'], unique=False)
    op.create_index(op.f('ix_blogs_author_id'), 'blogs', ['author_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_blogs_author_id'), table_name='blogs')
    op.drop_index(op.f('ix_blogs_client_id'), table_name='blogs')
    op.drop_index(op.f('ix_blogs_slug'), table_name='blogs')
    op.drop_table('blogs')

    op.drop_index(op.f('ix_clients_domain'), table_name='clients')
    op.drop_table('clients')
