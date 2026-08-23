"""Five mode restructure with new columns and data

Revision ID: b1234567890ab
Revises: a7baee5ef74e
Create Date: 2026-08-17 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b1234567890ab'
down_revision = 'a7baee5ef74e'
branch_labels = None
depends_on = None


def upgrade():
    # Delete all feedback first (depends on recordings)
    op.execute('DELETE FROM feedback')

    # Delete all recordings (depends on modes)
    op.execute('DELETE FROM recordings')

    # Delete all modes to clear old data
    op.execute('DELETE FROM modes')

    # Add new columns to modes table
    op.add_column('modes', sa.Column('slug', sa.String(), nullable=False))
    op.add_column('modes', sa.Column('default_timer_seconds', sa.Integer(), nullable=True))
    op.add_column('modes', sa.Column('accent_color', sa.String(), nullable=False))
    op.add_column('modes', sa.Column('sort_order', sa.Integer(), nullable=False, server_default='0'))

    # Create unique constraint on slug
    op.create_unique_constraint('uq_modes_slug', 'modes', ['slug'])

    # Insert the 5 new modes.
    # accent_color values are shades of the single brand hue (#DC9750), light to
    # dark by sort_order -- Nena uses one hue plus tints/shades, not a rainbow
    # per mode.
    modes_insert = [
        "INSERT INTO modes (name, description, slug, default_timer_seconds, accent_color, sort_order) VALUES ('Random Topic', 'An opinion or exploration prompt. The general-purpose mode.', 'random-topic', 60, '#E2A461', 1)",
        "INSERT INTO modes (name, description, slug, default_timer_seconds, accent_color, sort_order) VALUES ('Interview Prep', 'Tech interview questions, weighted toward behavioral answers and explaining your own projects.', 'interview-prep', 90, '#DC9750', 2)",
        "INSERT INTO modes (name, description, slug, default_timer_seconds, accent_color, sort_order) VALUES ('Learn Vocabulary', 'A word is shown with definition and example sentence; the user must use it naturally in a short spoken answer.', 'learn-vocab', 30, '#BD7E3E', 3)",
        "INSERT INTO modes (name, description, slug, default_timer_seconds, accent_color, sort_order) VALUES ('Read Aloud', 'An original passage to read for pace, clarity, and articulation.', 'read-aloud', NULL, '#966333', 4)",
        "INSERT INTO modes (name, description, slug, default_timer_seconds, accent_color, sort_order) VALUES ('Daily Reflection', 'One prompt per calendar day, same for the whole day, rotating at local midnight.', 'daily-reflection', 60, '#734B27', 5)",
    ]

    for insert_stmt in modes_insert:
        op.execute(insert_stmt)


def downgrade():
    # Drop unique constraint on slug
    op.drop_constraint('uq_modes_slug', 'modes', type_='unique')

    # Drop new columns
    op.drop_column('modes', 'sort_order')
    op.drop_column('modes', 'accent_color')
    op.drop_column('modes', 'default_timer_seconds')
    op.drop_column('modes', 'slug')
