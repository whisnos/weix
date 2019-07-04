"""empty message

Revision ID: ef30c3f7c44d
Revises: 285f94d2c6a9
Create Date: 2019-07-04 11:14:08.291869

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ef30c3f7c44d'
down_revision = '285f94d2c6a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('app_error_log', 'referer_url',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('app_error_log', 'referer_url',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###