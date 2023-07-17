from sqlalchemy import Column, Integer, String, Date, Time
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TelegramReport(Base):
    __tablename__ = 'telegram_reports'

    id = Column(Integer, primary_key=True)
    index_station = Column(String)
    date_telegram = Column(Date)
    time_telegram = Column(Time)
    gauges_telegram = Column(String)