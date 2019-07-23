"""empty message

Revision ID: 41925b08bb79
Revises: 1fbf2bd81f01
Create Date: 2019-07-23 01:34:31.304121

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41925b08bb79'
down_revision = '1fbf2bd81f01'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('device',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('company', sa.String(), nullable=True),
    sa.Column('sin', sa.Integer(), nullable=True),
    sa.Column('channel_num', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('patient',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=True),
    sa.Column('full_name', sa.String(), nullable=True),
    sa.Column('height', sa.String(), nullable=True),
    sa.Column('weight', sa.String(), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('address', sa.Text(), nullable=True),
    sa.Column('birthdate', sa.Date(), nullable=True),
    sa.Column('sex', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recording',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('instituition', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('time_description', sa.String(), nullable=True),
    sa.Column('visit_num', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('signal',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('sensor', sa.String(), nullable=True),
    sa.Column('sensor_location_on_body', sa.String(), nullable=True),
    sa.Column('raw', sa.ARRAY(sa.Float()), nullable=True),
    sa.Column('filtered', sa.ARRAY(sa.Float()), nullable=True),
    sa.Column('device_id', sa.Integer(), nullable=True),
    sa.Column('patient_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['device_id'], ['device.id'], ),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('channel_num', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('start_time', sa.Time(), nullable=True),
    sa.Column('end_time', sa.Time(), nullable=True),
    sa.Column('duration', sa.Float(), nullable=True),
    sa.Column('fs', sa.Integer(), nullable=True),
    sa.Column('unit', sa.String(), nullable=True),
    sa.Column('signal_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['signal_id'], ['signal.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('epoch',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('start_time', sa.Time(), nullable=False),
    sa.Column('end_time', sa.Time(), nullable=False),
    sa.Column('duration', sa.Float(), nullable=True),
    sa.Column('signal_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['signal_id'], ['signal.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('epoch')
    op.drop_table('data')
    op.drop_table('signal')
    op.drop_table('recording')
    op.drop_table('patient')
    op.drop_table('device')
    # ### end Alembic commands ###
