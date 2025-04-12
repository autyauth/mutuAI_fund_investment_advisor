from enum import Enum
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pendulum import timezone

class PeriodsEnum(Enum):
    one_year = 1
    three_year = 3
    five_year = 5
    ten_year = 10

class RocPeriodsEnum(Enum):
    three_month = "three_month"
    six_month = "six_month"
    ytd = "ytd"
    one_year = "one_year"
    three_year = "three_year"
    five_year = "five_year"
    ten_year = "ten_year"

def get_past_date(period: PeriodsEnum) -> datetime:
    tz = timezone('Asia/Bangkok')
    today = datetime.now(tz)
    
    # ย้อนปีไปตาม PeriodsEnum
    past_date = today - relativedelta(years=period.value)
    return past_date

def get_roc_past_date(period: RocPeriodsEnum, today: datetime) -> datetime:
    

    if period == RocPeriodsEnum.three_month:
        past_date = today - relativedelta(months=3)
    elif period == RocPeriodsEnum.six_month:
        past_date = today - relativedelta(months=6)
    elif period == RocPeriodsEnum.ytd:
        past_date = today.replace(month=1, day=1)
    elif period == RocPeriodsEnum.one_year:
        past_date = get_past_date(PeriodsEnum.one_year)
    elif period == RocPeriodsEnum.three_year:
        past_date = get_past_date(PeriodsEnum.three_year)
    elif period == RocPeriodsEnum.five_year:
        past_date = get_past_date(PeriodsEnum.five_year)
    elif period == RocPeriodsEnum.ten_year:
        past_date = get_past_date(PeriodsEnum.ten_year)
    else:
        raise ValueError("Invalid ROC period")
    
    return past_date