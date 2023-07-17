from fastapi import FastAPI
from sqlalchemy import Column, Integer, String, Date, Time, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from fastapi_sqlalchemy import DBSessionMiddleware

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost:5432/db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)


Base = declarative_base()

# Клас для таблиці telegram_report
class TelegramReport(Base):
    __tablename__ = 'telegram_report'
    id_telegram = Column(Integer, primary_key=True)
    index_station = Column(String(10))
    date_telegram = Column(Date)
    time_telegram = Column(Time)
    gauges_telegram = Column(String)

# Клас для таблиці measured_data
class MeasuredData(Base):
    __tablename__ = 'measured_data'
    id = Column(Integer, primary_key=True)
    index_station = Column(String(10))
    date_measured = Column(Date)
    time_measured = Column(Time)
    water_level = Column(Float)
    water_temperature = Column(Float)
    air_temperature = Column(Float)
    precipitation = Column(Float)
    water_surface_status = Column(String(50))

# Параметри підключення до бази даних PostgreSQL
database_uri = 'postgresql://postgres:password@db:5432/db'

# Створення з'єднання з базою даних

session = Session()

def save_data_to_table(index, data):
    table_name = f'database_{index}.telegram_report'
    # Отримання відповідної таблиці за назвою
    table = Base.metadata.tables[table_name]
    # Запис даних
    session = Session()
    session.execute(table.insert().values(data))
    session.commit()
    session.close()
