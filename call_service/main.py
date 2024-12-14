from flask import Flask, jsonify, request
import os
import dotenv

app = Flask(__name__)

# Импортируем модели, чтобы они регистрировались в SQLAlchemy
from models import Call,start_db,session
# Создаем таблицы, если их нет
@app.before_request
def create_tables():
    """
    Перед каждым запросом проверяем наличие таблиц в базе данных.
    Если таблиц нет, они будут автоматически созданы.
    """
    start_db()

@app.get("/")
def home():
    return "Welcome by call_service!"

from datetime import datetime

@app.post("/call/")
def call():
    """
    Создает запись о новом звонке в базе данных.
    
    Ожидает JSON-данные с ключами:
    - 'username' (обязательный): имя пользователя, совершившего звонок
    - 'status' (обязательный): статус звонка (например, 'completed', 'false', 'yes')
    - 'date' (необязательный): дата звонка в формате ISO 8601

    Возвращает:
    - ID звонка, имя пользователя, дату и статус.
    """
    data = request.json
    if not data or 'username' not in data or 'status' not in data:
        return jsonify({"message": "Username and status are required!"}), 400

    # Приведение статуса к булевому типу
    status = data['status'].lower() in ['true', 'completed', 'yes']

    # Используем текущую дату и время, если 'date' отсутствует
    date = data.get('date')
    if date:
        try:
            date = datetime.fromisoformat(date)
        except ValueError:
            return jsonify({"message": "Invalid date format. Use ISO 8601."}), 400
    else:
        date = None  # SQLAlchemy подставит значение по умолчанию

    new_call = Call(username=data['username'], date=date, status=status)
    session.add(new_call)
    session.commit()  # Сохраняем запись в базе данных
    return jsonify({"id": new_call.id, "username": new_call.username, "date": new_call.date, "status": new_call.status}), 201




@app.get("/call/history/")
def history():
    """
    Возвращает всю историю звонков из базы данных.
    Каждая запись включает:
    - ID звонка
    - Имя пользователя
    - Дата звонка
    - Статус звонка
    """
    all_calls = session.query(Call).all()  # Получаем всю историю звонков
    return jsonify([{"id": call.id, "username": call.username, "date": call.date, "status": call.status} for call in all_calls])

@app.get("/call/history/last/")
def get_call_last_some():
    """
    Возвращает данные о последнем звонке.

    Если записей в базе данных нет, возвращает сообщение с ошибкой.
    """
    last_call = session.query(Call).order_by(Call.date.desc()).first()  # Получаем последний звонок
    if last_call:
        return jsonify({"id": last_call.id, "username": last_call.username, "date": last_call.date, "status": last_call.status})
    return jsonify({"message": "No calls found."}), 404


    