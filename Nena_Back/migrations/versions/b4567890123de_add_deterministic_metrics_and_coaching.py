"""Add deterministic metrics and LLM coaching columns to Feedback.

Revision ID: b4567890123de
Revises: b3456789012cd
Create Date: 2026-08-18 13:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'b4567890123de'
down_revision = 'b3456789012cd'
branch_labels = None
depends_on = None


def upgrade():
    # Add deterministic metric columns
    op.add_column('feedback', sa.Column('hedge_count', sa.Integer(), nullable=True))
    op.add_column('feedback', sa.Column('hedge_list', postgresql.JSON(), nullable=True))
    op.add_column('feedback', sa.Column('time_to_point_seconds', sa.Float(), nullable=True))
    op.add_column('feedback', sa.Column('concreteness_ratio', sa.Float(), nullable=True))
    op.add_column('feedback', sa.Column('long_pause_count', sa.Integer(), nullable=True))

    # Add LLM coaching columns
    op.add_column('feedback', sa.Column('coach_notes', postgresql.JSON(), nullable=True))
    op.add_column('feedback', sa.Column('focus_area', sa.String(), nullable=True))
    op.add_column('feedback', sa.Column('focus_reason', sa.String(), nullable=True))
    op.add_column('feedback', sa.Column('framework_adherence', postgresql.JSON(), nullable=True))
    op.add_column('feedback', sa.Column('landing_strength', sa.String(), nullable=True))
    op.add_column('feedback', sa.Column('strongest_moment', sa.String(), nullable=True))
    op.add_column('feedback', sa.Column('next_topic_id', sa.Integer(), nullable=True))

    # Add foreign key for next_topic_id
    op.create_foreign_key('fk_feedback_next_topic_id', 'feedback', 'topics',
                          ['next_topic_id'], ['id'])


def downgrade():
    # Remove foreign key
    op.drop_constraint('fk_feedback_next_topic_id', 'feedback', type_='foreignkey')

    # Drop all new columns
    op.drop_column('feedback', 'next_topic_id')
    op.drop_column('feedback', 'strongest_moment')
    op.drop_column('feedback', 'landing_strength')
    op.drop_column('feedback', 'framework_adherence')
    op.drop_column('feedback', 'focus_reason')
    op.drop_column('feedback', 'focus_area')
    op.drop_column('feedback', 'coach_notes')
    op.drop_column('feedback', 'long_pause_count')
    op.drop_column('feedback', 'concreteness_ratio')
    op.drop_column('feedback', 'time_to_point_seconds')
    op.drop_column('feedback', 'hedge_list')
    op.drop_column('feedback', 'hedge_count')
