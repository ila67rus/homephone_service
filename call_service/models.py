   
from sqlalchemy import create_engine, Column, Integer, String,DateTime,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime,timezone
import dotenv
dotenv.load_dotenv()
import os

url_db=os.getenv("SQLALCHEMY_DATABASE_URI")
print(url_db)
engine = create_engine(url_db)

# Создаем базовый класс для моделей
Base = declarative_base()

# Настраиваем сессию для взаимодействия с базой данных
Session = sessionmaker(bind=engine)
session = Session()


# Пример модели  
class Call(Base):  
    __tablename__ = 'calls' 
    id = Column(Integer, primary_key=True)  
    username = Column(String(80), unique=True, nullable=False)  
    date = Column(DateTime,default=lambda: datetime.now(timezone.utc))
    status = Column(Boolean,nullable=False)
    
    def __repr__(self):
        return f'<Call(username={self.username}, date={self.data} , status = {self.status})>'


def start_db():
    Base.metadata.create_all(engine)