from flask import Flask, jsonify, request
import os
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)


# Импортируем модели, чтобы они регистрировались в SQLAlchemy
from models import User,start_db,session

# Создаем таблицы, если их нет
@app.before_request
def create_tables():
    start_db()


@app.get("/")
def home():
    return "Welcome by user_service!"

# GET /users — Получение списка всех пользователей
@app.get("/users/")
def users():
    """
    Извлекает список всех пользователей из базы данных.
    Возвращает список пользователей с их id, именем и телефоном.
    """
    all_users = session.query(User).all()  # Используем session.query для получения всех пользователей
    return jsonify([{"id": user.id, "name": user.username, "phone": user.phone} for user in all_users])


@app.get("/users/<int:user_id>")
def get_user(user_id):
    """
    Извлекает данные пользователя по его ID.
    Если пользователь найден, возвращает его id, имя и телефон.
    Если пользователь не найден, возвращает ошибку 404.
    """
    user = session.get(User, user_id)  # Используем явный запрос через сессию
    if user:
        return jsonify({"id": user.id, "name": user.username, "phone": user.phone})
    return jsonify({"message": "User not found"}), 404

    

# POST /users — Создание нового пользователя
@app.post("/users/")
def create_user():
    """
    Создаёт нового пользователя в базе данных.
    Ожидает JSON с параметрами:
    - 'name': имя пользователя (обязательно)
    - 'phone': телефон пользователя (обязательно)
    Если данные не указаны, возвращает ошибку 400.
    """
    data = request.json  # Получаем данные из тела запроса
    if not data or 'name' not in data or 'phone' not in data:
        return jsonify({"message": "Name and phone are required!"}), 400

    new_user = User(username=data['name'], phone=data['phone'])  # Создаем нового пользователя
    session.add(new_user)
    session.commit()  # Сохраняем нового пользователя в базе
    return jsonify({"id": new_user.id, "name": new_user.username, "phone": new_user.phone}), 201

# DELETE /users — Удаление пользователя по ID
@app.delete("/users/<int:user_id>")
def remove_user(user_id):
    """
    Удаляет пользователя по ID из базы данных.
    Если пользователь найден, он удаляется, и возвращается сообщение об успешном удалении.
    Если пользователь не найден, возвращает ошибку 404.
    """
    user = session.get(User, user_id)  # Находим пользователя по ID
    if user:
        session.delete(user)
        session.commit()  # Удаляем пользователя из базы данных
        return jsonify({"message": "User deleted successfully."}), 200
    else:
        return jsonify({"message": "User not found!"}), 404



    