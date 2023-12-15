"""Adding support for file upload

Revision ID: 853343c37c29
Revises: 3d76c31851df
Create Date: 2023-12-15 04:20:47.032421

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '853343c37c29'
down_revision = '3d76c31851df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('medical_record_documents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=255), nullable=False),
    sa.Column('path', sa.String(length=255), nullable=False),
    sa.Column('medical_record_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['medical_record_id'], ['medical_records.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('medical_record_documents')
    # ### end Alembic commands ###
