"""Added fields to event

Revision ID: 5a00d4f6aeb2
Revises: b2cfada3abcd
Create Date: 2019-12-03 18:03:56.390741

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a00d4f6aeb2'
down_revision = 'b2cfada3abcd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Events', sa.Column('flag_format', sa.String(length=64), nullable=False))
    op.add_column('Events', sa.Column('front_page', sa.Text(), nullable=False))
    op.add_column('Events', sa.Column('is_open', sa.Boolean(), nullable=False))
    op.add_column('Events', sa.Column('is_visible', sa.Boolean(), nullable=False))
    op.add_column('Events', sa.Column('url', sa.String(length=255), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Events', 'url')
    op.drop_column('Events', 'is_visible')
    op.drop_column('Events', 'is_open')
    op.drop_column('Events', 'front_page')
    op.drop_column('Events', 'flag_format')
    # ### end Alembic commands ###