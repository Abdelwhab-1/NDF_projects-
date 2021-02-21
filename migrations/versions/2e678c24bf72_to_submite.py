"""to submite 

Revision ID: 2e678c24bf72
Revises: 935f33cd9f39
Create Date: 2021-02-21 20:08:10.865626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e678c24bf72'
down_revision = '935f33cd9f39'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'website')
    op.drop_column('Venue', 'image_link')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('image_link', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    op.add_column('Venue', sa.Column('website', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
