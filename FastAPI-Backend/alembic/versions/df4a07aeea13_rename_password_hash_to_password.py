"""Rename password_hash to password

Revision ID: df4a07aeea13
Revises: 261012b4a48c
Create Date: 2024-12-30 11:45:26.160610

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'df4a07aeea13'
down_revision: Union[str, None] = '261012b4a48c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column('users', 'password_hash', new_column_name='password')

def downgrade():
    op.alter_column('users', 'password', new_column_name='password_hash')
    # ### end Alembic commands ###
