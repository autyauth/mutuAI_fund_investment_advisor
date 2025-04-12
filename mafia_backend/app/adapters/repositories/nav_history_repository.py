from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import text
from adapters.repositories.interfaces.INav_history_repository import INavHistoryRepository
from adapters.models import NavHistoryModel
from adapters.exceptions import *
from datetime import datetime, date
from utils.helper import parse_date_to_str
from typing import BinaryIO
import pandas as pd
import logging
from typing import Optional
from sqlalchemy.orm.exc import StaleDataError
from sqlalchemy import func

class NavHistoryRepository(INavHistoryRepository):
    def __init__(self, database):
        self.database = database
        self.logger = logging.getLogger(__name__)
    
    def get_nav_history_by_fund_name_and_date(self, fund_name: str, date: date) -> NavHistoryModel:
        session: Session = self.database.Session()
        try:
            nav_history = (
                session.query(NavHistoryModel)
                .filter(NavHistoryModel.fund_name == fund_name, NavHistoryModel.date == date)
                .first()
            )
            if nav_history is None:
                date_str = parse_date_to_str(date)
                raise RecordNotFoundException(f"Nav history '{fund_name}' on {date_str} not found")
            return nav_history
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving nav history: {str(e)}")
            raise DatabaseException("Failed to retrieve nav history by fund name and date", e)
        finally:
            session.close()
    
    def get_all_nav_history_by_fund_name(self, fund_name: str) -> list[NavHistoryModel]:
        session: Session = self.database.Session()
        try:
            nav_histories = (
                session.query(NavHistoryModel)
                .filter(NavHistoryModel.fund_name == fund_name)
                .order_by(NavHistoryModel.date.desc())
                .all()
            )
            return nav_histories
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving nav histories: {str(e)}")
            raise DatabaseException("Failed to retrieve all nav histories by fund name", e)
        finally:
            session.close()
        
    def get_nav_history_by_fund_name_and_date_range(self, fund_name: str, start_date: date, end_date: date) -> list[NavHistoryModel]:
        session: Session = self.database.Session()
        try:
            nav_histories = (
                session.query(NavHistoryModel)
                .filter(
                    NavHistoryModel.fund_name == fund_name,
                    NavHistoryModel.date >= start_date,
                    NavHistoryModel.date <= end_date
                )
                .order_by(NavHistoryModel.date.desc())
                .all()
            )
            return nav_histories
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving nav histories by date range: {str(e)}")
            raise DatabaseException("Failed to retrieve nav histories by fund name and date range", e)
        finally:
            session.close()

    def get_nav_history_by_date(self, date: date) -> list[NavHistoryModel]:
        session: Session = self.database.Session()
        try:
            nav_histories = (
                session.query(NavHistoryModel)
                .filter(NavHistoryModel.date == date)
                .order_by(NavHistoryModel.fund_name)
                .all()
            )
            return nav_histories
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving nav histories by date: {str(e)}")
            raise DatabaseException("Failed to retrieve nav histories by date", e)
        finally:
            session.close()

    def get_all_nav_history(self) -> list[NavHistoryModel]:
        session: Session = self.database.Session()
        try:
            nav_histories = (
                session.query(NavHistoryModel)
                .order_by(NavHistoryModel.date.desc(), NavHistoryModel.fund_name)
                .all()
            )
            return nav_histories
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving all nav histories: {str(e)}")
            raise DatabaseException("Failed to retrieve all nav histories", e)
        finally:
            session.close()
    
    def add_nav_history(self, nav_history: NavHistoryModel) -> None:
        session: Session = self.database.Session()
        try:
            session.add(nav_history)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            if "duplicate" in str(e.orig).lower():
                raise DuplicateEntryException(
                    f"Duplicate entry detected: {nav_history.fund_name} on {nav_history.date}", e
                )
            raise DatabaseException("Integrity error occurred while adding nav history", e)
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Database error while adding nav history: {str(e)}")
            raise DatabaseException("Failed to add nav history", e)
        finally:
            session.close()
    
    def update_nav_history(self, fund_name: str, date: date, nav_history: NavHistoryModel) -> None:
        session: Session = self.database.Session()
        try:
            existed_nav_history = (
                session.query(NavHistoryModel)
                .filter(
                    NavHistoryModel.fund_name == fund_name,
                    NavHistoryModel.date == date
                )
                .first()
            )
            
            if existed_nav_history is None:
                date_str = parse_date_to_str(date)
                raise RecordNotFoundException(
                    f"Nav history '{fund_name}' on {date_str} not found for update"
                )

            for attr, value in nav_history.__dict__.items():
                if not attr.startswith("_") and value is not None:
                    setattr(existed_nav_history, attr, value)

            session.commit()
        except RecordNotFoundException:
            session.rollback()
            raise
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Database error while updating nav history: {str(e)}")
            raise DatabaseException("Failed to update nav history", e)
        finally:
            session.close()
    
    def create_or_update_nav_history(self, nav_history: NavHistoryModel) -> None:
        """สร้างหรืออัปเดต NAV History โดยใช้ SQLAlchemy"""
        session: Session = self.database.Session()
        try:
            # ค้นหาข้อมูลที่มีอยู่ในฐานข้อมูล
            existed_nav_history: Optional[NavHistoryModel] = (
                session.query(NavHistoryModel)
                .filter(
                    NavHistoryModel.fund_name == nav_history.fund_name,
                    NavHistoryModel.date == nav_history.date
                )
                .with_for_update()  # Lock row เพื่อป้องกัน race condition
                .first()
            )

            if existed_nav_history is None:
                # หากไม่มีข้อมูล ให้เพิ่มใหม่
                session.add(nav_history)
            else:
                # อัปเดตเฉพาะฟิลด์ที่ไม่ใช่ None
                for attr in NavHistoryModel.__table__.columns.keys():
                    new_value = getattr(nav_history, attr)
                    if new_value is not None:
                        setattr(existed_nav_history, attr, new_value)

            session.commit()
            session.refresh(existed_nav_history if existed_nav_history else nav_history)  # Refresh instance

        except (SQLAlchemyError, StaleDataError) as e:
            session.rollback()
            self.logger.error(f"Database error while creating or updating nav history: {str(e)}", exc_info=True)
            raise DatabaseException("Failed to create or update NAV history", e)

        finally:
            session.close()
            
    def delete_nav_history(self, fund_name: str, date: date) -> None:
        session: Session = self.database.Session()
        try:
            nav_history = (
                session.query(NavHistoryModel)
                .filter(
                    NavHistoryModel.fund_name == fund_name,
                    NavHistoryModel.date == date
                )
                .first()
            )
            
            if nav_history is None:
                date_str = parse_date_to_str(date)
                raise RecordNotFoundException(
                    f"Nav history '{fund_name}' on {date_str} not found for deletion"
                )
            
            session.delete(nav_history)
            session.commit()
        except RecordNotFoundException:
            session.rollback()
            raise
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Database error while deleting nav history: {str(e)}")
            raise DatabaseException("Failed to delete nav history", e)
        finally:
            session.close()

    def delete_nav_history_by_fund(self, fund_name: str) -> None:
        session: Session = self.database.Session()
        try:
            session.execute(
                text("DELETE FROM nav_history WHERE fund_name = :fund_name"),
                {"fund_name": fund_name}
            )
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Database error while deleting nav history by fund: {str(e)}")
            raise DatabaseException("Failed to delete nav history by fund name", e)
        finally:
            session.close()

    def get_nav_history_latest_date(self, fund_name: str) -> NavHistoryModel:
        session: Session = self.database.Session()
        try:
            result = session.execute(
                text("""
                    SELECT *
                    FROM nav_history
                    WHERE fund_name = :fund_name
                    ORDER BY date DESC
                    LIMIT 1
                """),
                {"fund_name": fund_name}
            ).fetchone()

            if result:
                return NavHistoryModel(**dict(result._mapping))
            return None
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving latest nav history: {str(e)}")
            raise DatabaseException("Failed to retrieve latest nav history by fund name", e)
        finally:
            session.close()
    
    def get_nav_history_lastest_date_all_fund(self) -> list[NavHistoryModel]:
        session: Session = self.database.Session()
        try:
            result = session.execute(
                text("""
                SELECT t1.*
                FROM nav_history t1
                INNER JOIN (
                    SELECT fund_name, MAX(date) as max_date
                    FROM nav_history
                    GROUP BY fund_name
                ) t2
                ON t1.fund_name = t2.fund_name AND t1.date = t2.max_date
                """)
            ).fetchall()

            return [NavHistoryModel(**dict(row._mapping)) for row in result]
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving latest nav histories: {str(e)}")
            raise DatabaseException("Failed to retrieve latest nav histories of all funds", e)
        finally:
            session.close()

    def upload_nav_history_file(self, file: BinaryIO) -> None:
        session: Session = self.database.Session()
        try:
            df = pd.read_excel(file)
            required_columns = {"fund_name", "date", "nav", "fund_type", "selling_price", 
                              "redemption_price", "total_net_assets", "change"}
            if not required_columns.issubset(df.columns):
                raise ValueError(f"Missing required columns: {required_columns - set(df.columns)}")
            
            for _, row in df.iterrows():
                nav_history = NavHistoryModel(
                    fund_name=row["fund_name"],
                    date=row["date"] if isinstance(row["date"], datetime) else datetime.strptime(row["date"], '%Y-%m-%d'),
                    nav=row["nav"],
                    fund_type=row["fund_type"],
                    selling_price=row.get("selling_price"),
                    redemption_price=row.get("redemption_price"),
                    total_net_assets=row.get("total_net_assets"),
                    change=row.get("change")
                )
                session.add(nav_history)
            
            session.commit()
        except Exception as e:
            session.rollback()
            self.logger.error(f"Error uploading nav history file: {str(e)}")
            raise DatabaseException("Failed to upload nav history file", e)
        finally:
            session.close()
            
    def get_nav_history_by_fund_name_and_window(self, fund_name: str, window: int) -> list[NavHistoryModel]:
        session: Session = self.database.Session()
        try:
            nav_histories = (
                session.query(NavHistoryModel)
                .filter(NavHistoryModel.fund_name == fund_name)
                .order_by(NavHistoryModel.date.desc())
                .limit(window)
                .all()
            )
            return nav_histories
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving nav histories by window: {str(e)}")
            raise DatabaseException("Failed to retrieve nav histories by fund name and window", e)
        finally:
            session.close()
    def get_nav_history_by_fund_name_and_window_nav_date(self, fund_name: str, window: int, end_date: datetime) -> list[dict]:
        session: Session = self.database.Session()
        try:
            nav_histories = (
                session.query(
                    func.date_format(NavHistoryModel.date, "%Y-%m-%d").label("date"),  # แปลงวันที่เป็น string ที่ MySQL
                    NavHistoryModel.nav
                )
                .filter(
                    NavHistoryModel.fund_name == fund_name,
                    NavHistoryModel.date <= end_date
                )
                .order_by(NavHistoryModel.date.desc())
                .limit(window)
                .all()
            )

            return [{"date": nav.date, "nav": nav.nav} for nav in nav_histories]  # คืนค่า list ของ dict

        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving nav histories by window: {str(e)}")
            raise DatabaseException("Failed to retrieve nav histories by fund name and window", e)
        finally:
            session.close()
    
    def get_nearest_nav_after_date(self, fund_name: str, date: date) -> NavHistoryModel:
        session: Session = self.database.Session()
        try:
            nav_history = (
                session.query(NavHistoryModel)
                .filter(NavHistoryModel.fund_name == fund_name, NavHistoryModel.date >= date)
                .order_by(NavHistoryModel.date.asc())
                .first()
            )
            if nav_history is None:
                date_str = parse_date_to_str(date)
                raise RecordNotFoundException(f"Nav history '{fund_name}' on or before {date_str} not found")
            return nav_history
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving nav history: {str(e)}")
            raise DatabaseException("Failed to retrieve nav history by fund name and date or before", e)
        finally:
            session.close()