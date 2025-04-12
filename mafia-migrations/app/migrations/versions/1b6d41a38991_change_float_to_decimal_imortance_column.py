"""change float to decimal in portfolio and goal

Revision ID: 1b6d41a38991
Revises: 1b6d41a38990
Create Date: 2025-03-30

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Integer, String, DECIMAL, Float, text


# revision identifiers, used by Alembic.
revision: str = '1b6d41a38991'
down_revision: Union[str, None] = '1b6d41a38990'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # portfolio table
    op.alter_column('portfolio', 'gain_loss_percent', type_=sa.DECIMAL(10, 2))
    op.alter_column('portfolio', 'gain_loss_value', type_=sa.DECIMAL(10, 2))
    op.alter_column('portfolio', 'holding_units', type_=sa.DECIMAL(10, 4))
    op.alter_column('portfolio', 'holding_value', type_=sa.DECIMAL(10, 2))
    op.alter_column('portfolio', 'cost', type_=sa.DECIMAL(10, 2))
    op.alter_column('portfolio', 'total_profit', type_=sa.DECIMAL(10, 2))
    op.alter_column('portfolio', 'nav_average', type_=sa.DECIMAL(10, 4))
    op.alter_column('portfolio', 'present_nav', type_=sa.DECIMAL(10, 4))
    op.alter_column('portfolio', 'valid_units', type_=sa.DECIMAL(10, 4))

    # goal table
    op.alter_column('goal', 'users_goal', type_=sa.DECIMAL(10, 2))
    op.alter_column('goal', 'rate_fund', type_=sa.DECIMAL(10, 4))
    op.alter_column('goal', 'std_fund', type_=sa.DECIMAL(10, 4))
    op.alter_column('goal', 'rmf_amount_invested', type_=sa.DECIMAL(10, 2))
    op.alter_column('goal', 'ssf_amount_invested', type_=sa.DECIMAL(10, 2))
    op.alter_column('goal', 'thaiesg_amount_invested', type_=sa.DECIMAL(10, 2))

    # tax table
    op.alter_column('tax', 'users_tax', type_=sa.DECIMAL(10, 2))
    
    # transactions table
    op.alter_column('transactions', 'units_processed', type_=sa.DECIMAL(10, 4))
    op.alter_column('transactions', 'amount_processed', type_=sa.DECIMAL(10, 2))
    op.alter_column('transactions', 'processed_nav', type_=sa.DECIMAL(10, 4))
    op.alter_column('transactions', 'gain_loss_percent', type_=sa.DECIMAL(10, 2))
    op.alter_column('transactions', 'gain_loss_value', type_=sa.DECIMAL(10, 2))
    op.alter_column('transactions', 'changed_gl_percent', type_=sa.DECIMAL(10, 2))


def downgrade():
    # portfolio table
    op.alter_column('portfolio', 'gain_loss_percent', type_=sa.Float(precision=10))
    op.alter_column('portfolio', 'gain_loss_value', type_=sa.Float(precision=10))
    op.alter_column('portfolio', 'holding_units', type_=sa.Float(precision=10))
    op.alter_column('portfolio', 'holding_value', type_=sa.Float(precision=10))
    op.alter_column('portfolio', 'cost', type_=sa.Float(precision=10))
    op.alter_column('portfolio', 'total_profit', type_=sa.Float(precision=10))
    op.alter_column('portfolio', 'nav_average', type_=sa.Float(precision=10))
    op.alter_column('portfolio', 'present_nav', type_=sa.Float(precision=10))
    op.alter_column('portfolio', 'valid_units', type_=sa.Float(precision=10))

    # goal table
    op.alter_column('goal', 'users_goal', type_=sa.Float(precision=10))
    op.alter_column('goal', 'rate_fund', type_=sa.Float(precision=10))
    op.alter_column('goal', 'std_fund', type_=sa.Float(precision=10))
    op.alter_column('goal', 'rmf_amount_invested', type_=sa.DECIMAL(10, 2))
    op.alter_column('goal', 'ssf_amount_invested', type_=sa.DECIMAL(10, 2))
    op.alter_column('goal', 'thaiesg_amount_invested', type_=sa.DECIMAL(10, 2))

    # tax table
    op.alter_column('tax', 'users_tax', type_=sa.DECIMAL(10, 2))
    
    # transactions table
    op.alter_column('transactions', 'units_processed', type_=sa.Float(precision=10))
    op.alter_column('transactions', 'amount_processed', type_=sa.Float(precision=10))
    op.alter_column('transactions', 'processed_nav', type_=sa.Float(precision=10))
    op.alter_column('transactions', 'gain_loss_percent', type_=sa.Float(precision=10))
    op.alter_column('transactions', 'gain_loss_value', type_=sa.Float(precision=10))
    op.alter_column('transactions', 'changed_gl_percent', type_=sa.Float(precision=10))
