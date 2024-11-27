from sqlalchemy import create_engine, Column, Integer, String
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



class User(Base):  
    __tablename__ = 'users'  # Указываем имя таблицы
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    phone = Column(String(80), unique=True, nullable=False)

    
    def __repr__(self):
        return f'<User(username={self.username}, phone={self.phone})>'


def start_db():
    Base.metadata.create_all(engine)