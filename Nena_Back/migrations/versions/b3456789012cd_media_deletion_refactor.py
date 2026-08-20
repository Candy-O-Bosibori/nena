"""Media deletion refactor - remove video_url, add topic_id and framework_slug.

Revision ID: b3456789012cd
Revises: b2345678901bc
Create Date: 2026-08-18 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3456789012cd'
down_revision = 'b2345678901bc'
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns to recordings table
    op.add_column('recordings', sa.Column('topic_id', sa.Integer(), nullable=True))
    op.add_column('recordings', sa.Column('framework_slug', sa.String(), nullable=True))

    # Change duration_minutes from Integer to Float to store seconds
    op.alter_column('recordings', 'duration_minutes',
                    existing_type=sa.Integer(),
                    type_=sa.Float())

    # Drop video_url column
    op.drop_column('recordings', 'video_url')

    # Add foreign key constraint for topic_id
    op.create_foreign_key('fk_recordings_topic_id', 'recordings', 'topics',
                          ['topic_id'], ['id'])


def downgrade():
    # Remove foreign key constraint
    op.drop_constraint('fk_recordings_topic_id', 'recordings', type_='foreignkey')

    # Re-add video_url column
    op.add_column('recordings', sa.Column('video_url', sa.String(), nullable=True))

    # Change duration_minutes back to Integer
    op.alter_column('recordings', 'duration_minutes',
                    existing_type=sa.Float(),
                    type_=sa.Integer())

    # Drop new columns
    op.drop_column('recordings', 'framework_slug')
    op.drop_column('recordings', 'topic_id')
