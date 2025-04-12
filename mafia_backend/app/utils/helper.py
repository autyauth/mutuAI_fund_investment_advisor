from datetime import date, datetime, timedelta

def parse_date(date_str: str) -> date:
    return datetime.strptime(date_str, "%Y-%m-%d").date()

def parse_date_to_str(date: date) -> str:
    return date.strftime("%Y-%m-%d")
