"""add initial data to db

Revision ID: 1b6d41a38989
Revises: 9417ab3a5f66
Create Date: 2025-02-01 16:07:58.438134

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

data_path = Path(__file__).resolve().parent.parent.parent / "data"
nav_history_path = data_path / "nav_history"
mutual_funds_path = data_path / "mutual_funds"
portfolio_path = data_path / "portfolio"
transaction_path = data_path / "transactions"
users_path = data_path / "users"
goal_path = data_path / "goal"
sys.path.insert(0, str(data_path))



# revision identifiers, used by Alembic.
revision: str = '1b6d41a38989'
down_revision: Union[str, None] = '9417ab3a5f66'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    con = op.get_bind()
    # insert mutual_funds
    # fund_name,category,securities_industry,fund_type,fund_risk,dividend_policy,
    # redemption_fee,purchase_fee,fund_expense_ratio,minimum_initial_investment,
    # fund_registration_date,company,fund_fact,model_ml_info_path
    mutual_funds = pd.read_csv(mutual_funds_path / "mutual_funds.csv")
    mutual_funds['fund_name'] = mutual_funds['fund_name'].astype(str)
    mutual_funds['category'] = mutual_funds['category'].astype(str)
    mutual_funds['securities_industry'] = mutual_funds['securities_industry'].astype(str)
    mutual_funds['fund_type'] = mutual_funds['fund_type'].astype(str)
    mutual_funds['fund_risk'] = mutual_funds['fund_risk'].astype(str)
    mutual_funds['dividend_policy'] = mutual_funds['dividend_policy'].astype(str)
    mutual_funds['redemption_fee'] = mutual_funds['redemption_fee'].astype(float)
    mutual_funds['purchase_fee'] = mutual_funds['purchase_fee'].astype(float)
    mutual_funds['fund_expense_ratio'] = mutual_funds['fund_expense_ratio'].astype(float)
    mutual_funds['minimum_initial_investment'] = mutual_funds['minimum_initial_investment'].astype(int)
    mutual_funds['fund_registration_date'] = pd.to_datetime(mutual_funds['fund_registration_date'])
    mutual_funds['company'] = mutual_funds['company'].astype(str)
    mutual_funds['fund_fact'] = mutual_funds['fund_fact'].astype(str)
    mutual_funds['model_ml_info_path'] = mutual_funds['model_ml_info_path']
    
    mutual_funds.to_sql(
        "mutual_funds",
        con,
        if_exists="append",
        index=False,
        dtype={
            "fund_name": String(255),
            "category": String(255),
            "securities_industry": String(255),
            "fund_type": String(255),
            "fund_risk": String(2),
            "dividend_policy": String(255),
            "redemption_fee": Float,
            "purchase_fee": Float,
            "fund_expense_ratio": Float,
            "minimum_initial_investment": Integer,
            "fund_registration_date": sa.Date,
            "company": String(255),
            "fund_fact": String(255),
            "model_ml_info_path": String(255)
        }
    )
    
    # insert users
    users = pd.read_csv(users_path / "users.csv")
    users['birthday'] = pd.to_datetime(users['birthday'])
    users['username'] = users['username'].astype(str)
    users['password'] = users['password'].astype(str)
    users['email'] = users['email'].astype(str)
    users['telephone_number'] = users['telephone_number'].astype(str)
    users['job'] = users['job'].astype(str)

    users.to_sql(
        "users",
        con,
        if_exists="append",
        index=False,
        dtype={
            "username": String(255),
            "password": String(255),
            "email": String(255),
            "telephone_number": String(255),
            "birthday": sa.Date,
            "job": String(255),
            "salary": DECIMAL(10, 2),
            "risk_level": Integer,
        }
    )
    
    goal = pd.read_csv(goal_path / "goal.csv")
    goal['username'] = goal['username'].astype(str)
    goal['year'] = goal['year'].astype(int)
    goal['users_goal'] = goal['users_goal'].astype(float)
    goal['rate_fund'] = goal['rate_fund'].astype(float)
    goal['std_fund'] = goal['std_fund'].astype(float)
    
    goal.to_sql(
        "goal",
        con,
        if_exists="append",
        index=False,
        dtype={
            "username": String(255),
            "year": Integer,
            "users_goal": Float(10, 2),
            "rate_fund": Float(10, 2),
            "std_fund": Float(10, 2)
        }
    )
    
    columns_mapping_nav_history = {
        "Date": "date",
        "Total NAV": "total_net_assets",
        "NAV": "nav",
        "Sell NAV": "selling_price",
        "Buy NAV": "redemption_price",
        "Change": "change"
    }
    funds_data = []  # List สำหรับเก็บข้อมูลทั้งหมด
    files = [file for file in os.listdir(nav_history_path) if file.endswith('.csv')]

    for file in files:
        # อ่านเฉพาะคอลัมน์ที่ต้องการ
        data = pd.read_csv(
            nav_history_path / file, 
            usecols=["Date", "Total NAV", "NAV", "Sell NAV", "Buy NAV", "Change"]
        )
        # Mapping คอลัมน์
        data.rename(columns=columns_mapping_nav_history, inplace=True)
        data["fund_name"] = file.split(".")[0]
        data["fund_type"] = mutual_funds[mutual_funds["fund_name"] == data["fund_name"].iloc[0]]["fund_type"].iloc[0]
        
        # เพิ่มข้อมูลใน list
        funds_data.append(data)

    # รวมข้อมูลทั้งหมดใน DataFrame เดียว
    all_data = pd.concat(funds_data, ignore_index=True)
    all_data["date"] = pd.to_datetime(all_data["date"])
    all_data["fund_name"] = all_data["fund_name"].astype(str)
    all_data["fund_type"] = all_data["fund_type"].astype(str)
    # เขียนลงฐานข้อมูลครั้งเดียว
    all_data.to_sql(
        "nav_history",
        con,
        if_exists="append",
        index=False,
        dtype={
            "fund_name": String(255),
            "date": sa.Date,
            "nav": DECIMAL(10, 4),
            "fund_type": String(255),
            "selling_price": DECIMAL(10, 4),
            "redemption_price": DECIMAL(10, 4),
            "total_net_assets": DECIMAL(18, 2),
            "change": Float
        }
    )
    
    # portfolio
    portfolio = pd.read_csv(portfolio_path / "portfolio.csv")
    portfolio['username'] = portfolio['username'].astype(str)
    portfolio['fund_name'] = portfolio['fund_name'].astype(str)
    portfolio['fund_type'] = portfolio['fund_type'].astype(str)
    
    portfolio.to_sql(
        "portfolio",
        con,
        if_exists="append",
        index=False,
        dtype={
            "username": String(255),
            "fund_name": String(255),
            "fund_type": String(255),
            "gain_loss_percent": DECIMAL(10, 2),
            "gain_loss_value": DECIMAL(10, 2),
            "holding_units": DECIMAL(10, 2),
            "holding_value": DECIMAL(10, 2),
            "cost": DECIMAL(10, 2),
            "total_value": DECIMAL(10, 2),
            "nav_average": DECIMAL(10, 4),
            "present_nav": DECIMAL(10, 4),
            "valid_units": DECIMAL(10, 2)
        }
    )
    
    # insert transactions
    transactions = pd.read_csv(transaction_path / "transactions.csv")
    transactions['transaction_date'] = pd.to_datetime(transactions['transaction_date'])
    transactions['username'] = transactions['username'].astype(str)
    transactions['fund_name'] = transactions['fund_name'].astype(str)
    transactions['transaction_type'] = transactions['transaction_type'].astype(int)
    transactions.to_sql(
        "transactions",
        con,
        if_exists="append",
        index=False,
        dtype={
            "username": String(255),
            "fund_name": String(255),
            "transaction_type": Integer,
            "transaction_date": sa.Date,
            "units_processed": DECIMAL(10, 2),
            "amount_processed": DECIMAL(10, 2),
            "valid_to_sell": sa.Date,
            "processed_nav": Float(10, 4),
            "gain_loss_percent": Float(10, 2),
            "gain_loss_value": DECIMAL(10, 2),
            "changed_gl_percent": Float(10, 2)
        }
    )


def downgrade() -> None:
    con = op.get_bind()
    con.execute(text("DELETE FROM transactions"))
    con.execute(text("DELETE FROM portfolio"))
    con.execute(text("DELETE FROM nav_history"))
    con.execute(text("DELETE FROM notifications"))
    con.execute(text("DELETE FROM users"))
    con.execute(text("DELETE FROM mutual_funds"))
    con.execute(text("DELETE FROM goal"))
