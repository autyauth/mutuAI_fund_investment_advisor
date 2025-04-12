from enum import Enum
from datetime import datetime, timedelta

class AdviseEnum(Enum):
    """
    TREND_UP ->  FULL_BALANCE_MONTH -> BUY
    TREND_UP ->  UNFULL_BALANCE_MONTH -> BUY
    TREND_DOWN ->  FULL_BALANCE_MONTH -> HOLD
    TREND_DOWN ->  UNFULL_BALANCE_MONTH -> HOLD
    
    TREND_UP ->  FULL_BALANCE_YEAR -> HOLD
    TREND_UP ->  UNFULL_BALANCE_YEAR -> BUY
    TREND_DOWN ->  FULL_BALANCE_YEAR -> HOLD
    TREND_DOWN ->  UNFULL_BALANCE_YEAR -> HOLD
    """
    
    TREND_UP = "ราคามีแนวโน้มขึ้น"
    TREND_DOWN = "ยังไม่มีสัญญาณแนวโน้มขึ้น"
    
    FULL_BALANCE_MONTH = "คุณลงทุนครบจำนวนต่อเดือนแล้ว"
    FULL_BALANCE_YEAR = "คุณลงทุนครบจำนวนต่อปีแล้ว"
    
    UNFULL_BALANCE_MONTH  = "คุณยังลงทุนไม่ครบเป้าหมายของเดือนนี้"
    UNFULL_BALANCE_YEAR = "คุณยังลงทุนไม่ครบเป้าหมายของปีนี้"
    
    HOLD = "ควรชะลอการลงทุน"
    BUY = "เป็นช่วงเวลาที่ดีในการลงทุน"
    