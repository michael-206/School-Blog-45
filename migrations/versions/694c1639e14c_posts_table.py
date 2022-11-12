"""posts table

Revision ID: 694c1639e14c
Revises: cb657def14c4
Create Date: 2022-10-14 13:23:39.416232

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '694c1639e14c'
down_revision = 'cb657def14c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('author', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'author')
    # ### end Alembic commands ###