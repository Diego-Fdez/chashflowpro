"""add pg_trgm extension

Revision ID: 8b16d72c1970
Revises: cab5f8ebe860
Create Date: 2023-06-22 17:56:57.394057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b16d72c1970'
down_revision = 'cab5f8ebe860'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
