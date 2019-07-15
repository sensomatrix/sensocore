"""empty message

Revision ID: 01256a0967c9
Revises: 971d7c8fa0d8
Create Date: 2019-07-15 16:13:12.798244

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01256a0967c9'
down_revision = '971d7c8fa0d8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('data', sa.Column('signal_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'data', 'signal', ['signal_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'data', type_='foreignkey')
    op.drop_column('data', 'signal_id')
    # ### end Alembic commands ###
