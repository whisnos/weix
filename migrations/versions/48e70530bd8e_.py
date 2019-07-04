"""empty message

Revision ID: 48e70530bd8e
Revises: df86b7dd0819
Create Date: 2019-07-04 10:43:20.430177

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '48e70530bd8e'
down_revision = 'df86b7dd0819'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_app_access_log_uid', table_name='app_access_log')
    op.drop_column('app_access_log', 'uid')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('app_access_log', sa.Column('uid', mysql.BIGINT(display_width=20), autoincrement=False, nullable=False))
    op.create_index('ix_app_access_log_uid', 'app_access_log', ['uid'], unique=False)
    # ### end Alembic commands ###
