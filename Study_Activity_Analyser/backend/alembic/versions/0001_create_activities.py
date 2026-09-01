"""create activities table

Revision ID: 0001
Revises:
Create Date: 2026-08-31

"""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "activities",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column("domain", sa.String(), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("ended_at", sa.DateTime(), nullable=False),
        sa.Column("duration", sa.Float(), nullable=False),
        sa.Column("category", sa.String(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("classification_source", sa.String(), nullable=False),
        sa.Column("needs_review", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.drop_table("study_activities")


def downgrade() -> None:
    op.drop_table("activities")
    op.create_table(
        "study_activities",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String()),
        sa.Column("url", sa.String()),
        sa.Column("duration", sa.Float()),
        sa.Column("domain", sa.String()),
        sa.Column("confidence", sa.Float()),
        sa.Column("needs_review", sa.Boolean()),
    )