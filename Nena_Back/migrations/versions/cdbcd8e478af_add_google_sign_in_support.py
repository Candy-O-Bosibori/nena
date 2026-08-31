"""Add google_id to users and make password nullable for Google-only accounts

Revision ID: cdbcd8e478af
Revises: c5678901234ef
Create Date: 2026-08-30 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'cdbcd8e478af'
down_revision = 'c5678901234ef'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('google_id', sa.String(), nullable=True))
    op.create_unique_constraint('uq_users_google_id', 'users', ['google_id'])
    op.alter_column('users', 'password', existing_type=sa.String(), nullable=True)


def downgrade():
    op.alter_column('users', 'password', existing_type=sa.String(), nullable=False)
    op.drop_constraint('uq_users_google_id', 'users', type_='unique')
    op.drop_column('users', 'google_id')
