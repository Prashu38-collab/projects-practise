"""add subject and topic columns

Revision ID: 05b72a7c09fc
Revises: 0001
Create Date: 2026-08-31 18:52:24.217299

"""
from alembic import op
import sqlalchemy as sa


revision = '05b72a7c09fc'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('activities', schema=None) as batch_op:
        batch_op.add_column(sa.Column('subject', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('topic', sa.String(), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('activities', schema=None) as batch_op:
        batch_op.drop_column('topic')
        batch_op.drop_column('subject')
