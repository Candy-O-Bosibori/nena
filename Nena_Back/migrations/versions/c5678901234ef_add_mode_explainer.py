"""Add explainer column to modes for the Overview page header

Revision ID: c5678901234ef
Revises: 352e523c09d5
Create Date: 2026-08-22 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c5678901234ef'
down_revision = '352e523c09d5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('modes', sa.Column('explainer', sa.String(), nullable=True))

    # explainer is a longer, mode-specific "how to use this" paragraph shown
    # on the Overview page header. Kept separate from `description` (a short
    # one-liner also used as a fallback in Feedback.jsx's recording cards) so
    # lengthening this text doesn't leak into that unrelated UI.
    explainer_updates = [
        ("random-topic", "Take a few minutes to think about or research the topic you land on. Consider what you'd like to say, then hit record."),
        ("interview-prep", "Tech interview questions, weighted toward behavioral answers and explaining your own projects. Helps you talk about your work and experience."),
        ("learn-vocab", "A word is shown with its definition and an example sentence. Use it naturally in a short spoken answer, and let's build your vocabulary for future conversations."),
        ("read-aloud", "Pick a book or passage of your choice and read it aloud, for pace, clarity, and articulation."),
        ("daily-reflection", "One prompt a day about what you did today. Think of it like a daily journal, spoken instead of written."),
    ]

    conn = op.get_bind()
    for slug, explainer in explainer_updates:
        conn.execute(
            sa.text("UPDATE modes SET explainer = :explainer WHERE slug = :slug"),
            {"explainer": explainer, "slug": slug},
        )


def downgrade():
    op.drop_column('modes', 'explainer')
