"""empty message

Revision ID: e61ea004ab45
Revises: d3a0e057b706
Create Date: 2019-07-06 13:00:25.298559

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e61ea004ab45'
down_revision = 'd3a0e057b706'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('queue_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('queue_name', sa.String(length=30), nullable=False),
    sa.Column('data', sa.String(length=500), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('updated_time', sa.DateTime(), nullable=False),
    sa.Column('created_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('queue_list')
    # ### end Alembic commands ###