"""Teste de primeira migration

Revision ID: 962d88135b0c
Revises: 
Create Date: 2024-12-14 07:26:00.375438

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '962d88135b0c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_Tutor')
    with op.batch_alter_table('Tutor', schema=None) as batch_op:
        batch_op.add_column(sa.Column('senha', sa.String(length=128), nullable=False))
        batch_op.alter_column('cpf',
               existing_type=sa.VARCHAR(length=11),
               nullable=False)
        batch_op.alter_column('telefone',
               existing_type=sa.VARCHAR(length=11),
               nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Tutor', schema=None) as batch_op:
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
        batch_op.alter_column('telefone',
               existing_type=sa.VARCHAR(length=11),
               nullable=True)
        batch_op.alter_column('cpf',
               existing_type=sa.VARCHAR(length=11),
               nullable=True)
        batch_op.drop_column('senha')

    op.create_table('_alembic_tmp_Tutor',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('nome', sa.VARCHAR(length=40), nullable=False),
    sa.Column('nasc', sa.DATETIME(), nullable=False),
    sa.Column('cpf', sa.VARCHAR(length=11), nullable=False),
    sa.Column('telefone', sa.VARCHAR(length=11), nullable=False),
    sa.Column('email', sa.VARCHAR(length=255), nullable=False),
    sa.Column('senha', sa.VARCHAR(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cpf'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('telefone')
    )
    # ### end Alembic commands ###
