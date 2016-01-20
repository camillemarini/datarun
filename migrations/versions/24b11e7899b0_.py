"""empty message

Revision ID: 24b11e7899b0
Revises: None
Create Date: 2016-01-20 15:55:18.852263

"""

# revision identifiers, used by Alembic.
revision = '24b11e7899b0'
down_revision = None

from alembic import op
import sqlalchemy as sa
import datarun

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('raw_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('file_path', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('submission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('files_path', sa.String(length=200), nullable=True),
    sa.Column('raw_data_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['raw_data_id'], ['raw_data.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('submission_folds',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('submission_id', sa.Integer(), nullable=True),
    sa.Column('train_is', datarun.models.NumpyType(), nullable=False),
    sa.Column('test_is', datarun.models.NumpyType(), nullable=False),
    sa.Column('predictions', datarun.models.NumpyType(), nullable=True),
    sa.Column('state', sa.Enum('todo', 'done', 'error', name='state'), nullable=True),
    sa.Column('log_messages', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['submission_id'], ['submission.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('submission_folds')
    op.drop_table('submission')
    op.drop_table('raw_data')
    ### end Alembic commands ###
