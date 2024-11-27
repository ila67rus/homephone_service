
from datetime import datetime,timezone
from sqlalchemy import create_engine, Column, Integer, String,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import dotenv
dotenv.load_dotenv()
import os

engine = create_engine(os.getenv("SQLALCHEMY_DATABASE_URI"))

# Создаем базовый класс для моделей
Base = declarative_base()

# Настраиваем сессию для взаимодействия с базой данных
Session = sessionmaker(bind=engine)
session = Session()

# Функция для получения текущего времени в UTC с учетом временной зоны
def current_utc_time():
    return datetime.now(timezone.utc)

# Пример модели  
class UserLog(Base):
    __tablename__ = 'user_logs'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False)
    action = Column(String(200), nullable=False)
    timestamp = Column(DateTime, default=current_utc_time)

    def __repr__(self):
        return f'<UserLog(username={self.username}, action={self.action}, timestamp={self.timestamp})>'

# Модель для логов звонков
class CallLog(Base):
    __tablename__ = 'call_logs'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False)
    call_duration = Column(Integer, nullable=False)  # Длительность звонка в секундах
    status = Column(String(50), nullable=False)  # Статус звонка
    timestamp = Column(DateTime, default=current_utc_time)

    def __repr__(self):
        return f'<CallLog(username={self.username}, call_duration={self.call_duration}, status={self.status}, timestamp={self.timestamp})>'

def start_db():
    Base.metadata.create_all(engine)  