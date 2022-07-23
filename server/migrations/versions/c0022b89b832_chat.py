"""chat

Revision ID: c0022b89b832
Revises: 4cae381afbe4
Create Date: 2022-07-23 10:18:23.089188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0022b89b832'
down_revision = '4cae381afbe4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chat', sa.Column('chat_creator', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'chat', 'user', ['chat_creator'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'chat', type_='foreignkey')
    op.drop_column('chat', 'chat_creator')
    # ### end Alembic commands ###
