"""initial db

Revision ID: 9417ab3a5f66
Revises: 
Create Date: 2025-02-01 16:05:45.577577

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9417ab3a5f66'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mutual_funds',
    sa.Column('fund_name', sa.String(length=255), nullable=False),
    sa.Column('category', sa.String(length=255), nullable=True),
    sa.Column('securities_industry', sa.String(length=255), nullable=True),
    sa.Column('fund_type', sa.String(length=255), nullable=True),
    sa.Column('fund_risk', sa.String(length=255), nullable=True),
    sa.Column('dividend_policy', sa.String(length=255), nullable=True),
    sa.Column('redemption_fee', sa.Float(), nullable=True),
    sa.Column('purchase_fee', sa.Float(), nullable=True),
    sa.Column('fund_expense_ratio', sa.Float(), nullable=True),
    sa.Column('minimum_initial_investment', sa.Integer(), nullable=True),
    sa.Column('fund_registration_date', sa.Date(), nullable=True),
    sa.Column('company', sa.String(length=255), nullable=True),
    sa.Column('fund_fact', sa.String(length=255), nullable=True),
    sa.Column('model_ml_info_path', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('fund_name')
    )
    op.create_table('users',
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('telephone_number', sa.String(length=255), nullable=True),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.Column('job', sa.String(length=255), nullable=True),
    sa.Column('salary', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('risk_level', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('username')
    )
    op.create_table('deduction',
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('users_deduction', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('monthly_income', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('bonus', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('other_income', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('marital_status', sa.String(length=50), nullable=True),
    sa.Column('num_children', sa.Integer(), nullable=True),
    sa.Column('num_parents', sa.Integer(), nullable=True),
    sa.Column('num_disabled_dependents', sa.Integer(), nullable=True),
    sa.Column('social_security', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('life_insurance', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('health_insurance', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('parent_health_insurance', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('social_enterprise', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('thai_esg', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('rmf', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('ssf', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('pvd', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('gpf', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('nsf', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('pension_insurance', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('general_donation', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('education_donation', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('political_donation', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('easy_receipt', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('secondary_tourism', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('mortgage_interest', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('new_house_cost', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('pregnancy_expense', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.ForeignKeyConstraint(['username'], ['users.username'], ondelete="CASCADE"),
    sa.PrimaryKeyConstraint('username', 'year')
    )
    op.create_table('deduction_2025',
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('monthly_income', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('bonus_income', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('additional_income', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('personal_deduction', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('marital_deduction', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('child_deduction', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('parent_deduction', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('disable_deduction', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('prenatal_deduction', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('general_life_insurance', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('parent_life_insurance', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('self_life_insurance', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('provident_fund', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('pension_fund', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('rmf_fund', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('pension_life_insurance', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('national_saving_fund', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('housing_interest', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('social_enterprise', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('thai_esg', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('new_housing', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('easy_receipt', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('education_donation', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('general_donation', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('total_income', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('total_deduction', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('taxable_income', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.ForeignKeyConstraint(['username'], ['users.username'], ),
    sa.PrimaryKeyConstraint('username', 'year')
    )
    op.create_table('goal',
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('users_goal', sa.Float(precision=10, asdecimal=2), nullable=True),
    sa.Column('rate_fund', sa.Float(precision=10, asdecimal=2), nullable=True),
    sa.Column('std_fund', sa.Float(precision=10, asdecimal=2), nullable=True),
    sa.ForeignKeyConstraint(['username'], ['users.username'], ),
    sa.PrimaryKeyConstraint('username', 'year')
    )
    op.create_table('nav_history',
    sa.Column('fund_name', sa.String(length=255), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('nav', sa.Numeric(precision=10, scale=4), nullable=True),
    sa.Column('fund_type', sa.String(length=255), nullable=True),
    sa.Column('selling_price', sa.Numeric(precision=10, scale=4), nullable=True),
    sa.Column('redemption_price', sa.Numeric(precision=10, scale=4), nullable=True),
    sa.Column('total_net_assets', sa.Numeric(precision=18, scale=2), nullable=True),
    sa.Column('change', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['fund_name'], ['mutual_funds.fund_name'], ),
    sa.PrimaryKeyConstraint('fund_name', 'date')
    )
    op.create_table('notifications',
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('message', sa.String(length=255), nullable=False),
    sa.Column('timestamp', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('is_read', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['username'], ['users.username'], name='fk_notifications_username'),
    sa.PrimaryKeyConstraint('username', 'message')
    )
    op.create_table('perfomance_mutual_funds',
    sa.Column('fund_name', sa.String(length=255), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('std_three_month', sa.Float(), nullable=True),
    sa.Column('std_six_month', sa.Float(), nullable=True),
    sa.Column('std_one_year', sa.Float(), nullable=True),
    sa.Column('std_three_year', sa.Float(), nullable=True),
    sa.Column('std_five_year', sa.Float(), nullable=True),
    sa.Column('std_ten_year', sa.Float(), nullable=True),
    sa.Column('sharpe_ratio_three_month', sa.Float(), nullable=True),
    sa.Column('sharpe_ratio_six_month', sa.Float(), nullable=True),
    sa.Column('sharpe_ratio_one_year', sa.Float(), nullable=True),
    sa.Column('sharpe_ratio_three_year', sa.Float(), nullable=True),
    sa.Column('sharpe_ratio_five_year', sa.Float(), nullable=True),
    sa.Column('sharpe_ratio_ten_year', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['fund_name'], ['mutual_funds.fund_name'], ),
    sa.PrimaryKeyConstraint('fund_name', 'date')
    )
    op.create_table('portfolio',
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('fund_name', sa.String(length=255), nullable=False),
    sa.Column('fund_type', sa.String(length=255), nullable=True),
    sa.Column('gain_loss_percent', sa.Float(precision=10, asdecimal=2), nullable=True),
    sa.Column('gain_loss_value', sa.Float(precision=10, asdecimal=2), nullable=True),
    sa.Column('holding_units', sa.Float(precision=10, asdecimal=2), nullable=True),
    sa.Column('holding_value', sa.Float(precision=10, asdecimal=2), nullable=True),
    sa.Column('cost', sa.Float(precision=10, asdecimal=2), nullable=True),
    sa.Column('total_profit', sa.Float(precision=10, asdecimal=2), nullable=True),
    sa.Column('nav_average', sa.Float(precision=10, asdecimal=4), nullable=True),
    sa.Column('present_nav', sa.Float(precision=10, asdecimal=4), nullable=True),
    sa.Column('valid_units', sa.Float(precision=10, asdecimal=2), nullable=True),
    sa.ForeignKeyConstraint(['username'], ['users.username'], ),
    sa.PrimaryKeyConstraint('username', 'fund_name')
    )
    op.create_table('prediction_trend_funds',
    sa.Column('fund_name', sa.String(length=255), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('trend', sa.Integer(), nullable=True),
    sa.Column('up_trend_prob', sa.Float(), nullable=True),
    sa.Column('down_trend_prob', sa.Float(), nullable=True),
    sa.Column('reason', sa.String(length=255), nullable=True),
    sa.Column('indicator', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['fund_name'], ['mutual_funds.fund_name'], ),
    sa.PrimaryKeyConstraint('fund_name', 'date')
    )
    op.create_table('tax',
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('users_tax', sa.Float(precision=10, asdecimal=2), nullable=True),
    sa.ForeignKeyConstraint(['username'], ['users.username'], ),
    sa.PrimaryKeyConstraint('username', 'year')
    )
    op.create_table('transactions',
    sa.Column('transaction_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('fund_name', sa.String(length=255), nullable=True),
    sa.Column('transaction_type', sa.Integer(), nullable=True),
    sa.Column('transaction_date', sa.Date(), nullable=True),
    sa.Column('units_processed', sa.Float(precision=10, asdecimal=2), nullable=True),
    sa.Column('amount_processed', sa.Float(precision=10, asdecimal=2), nullable=True),
    sa.Column('valid_to_sell', sa.Date(), nullable=True),
    sa.Column('processed_nav', sa.Float(precision=10, asdecimal=4), nullable=True),
    sa.Column('gain_loss_percent', sa.Float(precision=10, asdecimal=2), nullable=True),
    sa.Column('gain_loss_value', sa.Float(precision=10, asdecimal=2), nullable=True),
    sa.Column('changed_gl_percent', sa.Float(precision=10, asdecimal=2), nullable=True),
    sa.ForeignKeyConstraint(['fund_name'], ['mutual_funds.fund_name'], ),
    sa.ForeignKeyConstraint(['username'], ['users.username'], ),
    sa.PrimaryKeyConstraint('transaction_id')
    )
    op.create_table('user_tokens',
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('token', sa.String(length=512), nullable=True),
    sa.Column('expires_at', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('username', 'token')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transactions')
    op.drop_table('tax')
    op.drop_table('prediction_trend_funds')
    op.drop_table('portfolio')
    op.drop_table('perfomance_mutual_funds')
    op.drop_table('notifications')
    op.drop_table('nav_history')
    op.drop_table('goal')
    op.drop_table('deduction_2025')
    op.drop_table('deduction')
    op.drop_table('users')
    op.drop_table('mutual_funds')
    # ### end Alembic commands ###
