"""add_column_goal_and_advisor.

Revision ID: 1b6d41a38990
Revises: 1b6d41a38989
Create Date: 2025-02-20 16:07:58.438134

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import os
import pandas as pd
import sys
from pathlib import Path
from sqlalchemy import Integer, String, DECIMAL, Float, text



# revision identifiers, used by Alembic.
revision: str = '1b6d41a38990'
down_revision: Union[str, None] = '1b6d41a38989'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Add columns to goal table
    op.add_column('goal', sa.Column('rmf_amount_invested', sa.DECIMAL(precision=10, scale=2), nullable=True))
    op.add_column('goal', sa.Column('ssf_amount_invested', sa.DECIMAL(precision=10, scale=2), nullable=True))
    op.add_column('goal', sa.Column('thaiesg_amount_invested', sa.DECIMAL(precision=10, scale=2), nullable=True))
    
    op.create_table('user_advise',
        sa.Column('username', sa.String(length=255), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('fund_name', sa.String(length=255), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.PrimaryKeyConstraint('username', 'year', 'fund_name'),
        
        # ตั้งชื่อ Foreign Key Constraints เพื่อให้ drop ได้ใน downgrade
        sa.ForeignKeyConstraint(
            ['username'], ['users.username'], 
            ondelete="CASCADE", name="fk_advisor_username"
        ),
        sa.ForeignKeyConstraint(
            ['fund_name'], ['mutual_funds.fund_name'], 
            ondelete="CASCADE", name="fk_advisor_fund_name"
        )
    )

def downgrade() -> None:
    # Drop Foreign Key Constraints first
    op.drop_constraint('fk_advisor_username', 'user_advise', type_='foreignkey')
    op.drop_constraint('fk_advisor_fund_name', 'user_advise', type_='foreignkey')

    # Drop advisor table
    op.drop_table('user_advise')

    # Drop columns in goal table
    op.drop_column('goal', 'rmf_amount_invested')
    op.drop_column('goal', 'ssf_amount_invested')
    op.drop_column('goal', 'thaiesg_amount_invested')
