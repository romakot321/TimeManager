"""compose minutes and text

Revision ID: 93c569a967b6
Revises: cdfdf49ce2b0
Create Date: 2023-07-27 00:34:43.732279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93c569a967b6'
down_revision = 'cdfdf49ce2b0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('minutes', sa.Integer(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_notes_user_id_users')),
    sa.PrimaryKeyConstraint('user_id', 'date', name=op.f('pk_notes'))
    )
    op.drop_index('ix_hours_id', table_name='hours')
    op.drop_table('hours')
    op.drop_index('ix_tasks_id', table_name='tasks')
    op.drop_table('tasks')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasks',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('text', sa.TEXT(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_tasks_user_id_users'),
    sa.PrimaryKeyConstraint('id', name='pk_tasks')
    )
    op.create_index('ix_tasks_id', 'tasks', ['id'], unique=False)
    op.create_table('hours',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('hours', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_hours_user_id_users'),
    sa.PrimaryKeyConstraint('id', name='pk_hours')
    )
    op.create_index('ix_hours_id', 'hours', ['id'], unique=False)
    op.drop_table('notes')
    # ### end Alembic commands ###
