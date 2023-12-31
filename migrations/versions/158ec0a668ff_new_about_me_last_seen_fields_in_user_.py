"""new about_me & last_seen fields in User model

Revision ID: 158ec0a668ff
Revises: f38ca892b614
Create Date: 2023-09-18 11:25:25.676016

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '158ec0a668ff'
down_revision = 'f38ca892b614'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('about_me', sa.String(length=140), nullable=True))
        batch_op.add_column(sa.Column('last_seen', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Users', schema=None) as batch_op:
        batch_op.drop_column('last_seen')
        batch_op.drop_column('about_me')

    # ### end Alembic commands ###
