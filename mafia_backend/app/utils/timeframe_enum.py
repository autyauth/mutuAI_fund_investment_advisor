from enum import Enum
from datetime import datetime, timedelta

class Timeframe(Enum):
    ONE_MONTH = "1m"
    SIX_MONTHS = "6m"
    YEAR_TO_DATE = "ytd"
    ONE_YEAR = "1y"
    MAX = "max"

    def get_date_range(self):
        """Return the start and end dates based on the timeframe."""
        today = datetime.now()
        if self == Timeframe.ONE_MONTH:
            return today - timedelta(days=30), today
        elif self == Timeframe.SIX_MONTHS:
            return today - timedelta(days=6 * 30), today
        elif self == Timeframe.YEAR_TO_DATE:
            return datetime(today.year, 1, 1), today
        elif self == Timeframe.ONE_YEAR:
            return today - timedelta(days=365), today
        elif self == Timeframe.MAX:
            return None, None  # No date filter
        else:
            raise ValueError("Invalid Timeframe")