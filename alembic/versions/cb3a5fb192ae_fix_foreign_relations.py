"""fix foreign relations

Revision ID: cb3a5fb192ae
Revises: d42264cd1a54
Create Date: 2025-02-17 14:19:16.642295

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'cb3a5fb192ae'
down_revision: Union[str, None] = 'd42264cd1a54'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('referral_code_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'referral_codes', ['referral_code_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'referral_code_id')
    # ### end Alembic commands ###
