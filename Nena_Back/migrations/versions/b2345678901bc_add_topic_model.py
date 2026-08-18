"""Add Topic model

Revision ID: b2345678901bc
Revises: b1234567890ab
Create Date: 2026-08-17 12:01:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b2345678901bc'
down_revision = 'b1234567890ab'
branch_labels = None
depends_on = None


def upgrade():
    # Create topics table
    op.create_table('topics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('mode_id', sa.Integer(), nullable=False),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('difficulty', sa.Enum('easy', 'medium', 'hard', name='topic_difficulty'), nullable=False),
        sa.Column('tags', postgresql.JSON(), nullable=False, server_default='[]'),
        sa.Column('meta', postgresql.JSON(), nullable=True, server_default='{}'),
        sa.Column('active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['mode_id'], ['modes.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create index on mode_id for faster lookups
    op.create_index('ix_topics_mode_id', 'topics', ['mode_id'])


def downgrade():
    # Drop index
    op.drop_index('ix_topics_mode_id', table_name='topics')

    # Drop table
    op.drop_table('topics')
