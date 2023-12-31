"""empty message

Revision ID: 598c96ee7dac
Revises: ef401ff690bd
Create Date: 2023-06-21 17:16:29.223672

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '598c96ee7dac'
down_revision = 'ef401ff690bd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('sub', sa.String(length=40), nullable=False))
    op.alter_column('users', 'phone_number',
               existing_type=sa.VARCHAR(length=15),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'phone_number',
               existing_type=sa.VARCHAR(length=15),
               nullable=False)
    op.drop_column('users', 'sub')
    # ### end Alembic commands ###
