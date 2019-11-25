"""Updated teams, added teamMembers and teamRequests

Revision ID: 80751781e230
Revises: 0159cc2d8db7
Create Date: 2019-11-16 12:31:28.091762

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '80751781e230'
down_revision = '0159cc2d8db7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('TeamMembers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('captain', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['team_id'], ['Teams.id'], 'TeamMembers_team_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], 'TeamMembers_user_id_fkey'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('TeamRequests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('requested_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['team_id'], ['Teams.id'], 'TeamRequests_team_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], 'TeamRequests_user_id_fkey'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('TeamRequests')
    op.drop_table('TeamMembers')
    # ### end Alembic commands ###
