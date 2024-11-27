from flask import Flask, jsonify, request
from redis import Redis
import json  # Для сериализации данных

app = Flask(__name__)

# Настройка подключения к Redis
cache = Redis(port=6379, db=0)

# Кэширование пользователя
@app.post("/cache/user")
def cache_user():
    """
    Кэширует данные пользователя в Redis.
    Ожидает JSON с ключами:
    - 'username': имя пользователя (обязательно)
    - 'phone': телефон пользователя (обязательно)

    Сохраняет данные пользователя в формате JSON, используя ключ 'user:<username>'.
    """
    data = request.json
    if not data or 'username' not in data or 'phone' not in data:
        return jsonify({"message": "Username and phone are required!"}), 400
    
    # Сериализуем данные пользователя в JSON строку
    user_data = json.dumps(data)
    
    # Сохраняем данные пользователя в Redis с уникальным ключом
    cache.set(f"user:{data['username']}", user_data)
    return jsonify({"message": f"User {data['username']} cached successfully!"}), 201

@app.get("/cache/user")
def get_user_from_cache():
    """
    Извлекает данные пользователя из Redis по его имени.
    Ожидает параметр 'username' в запросе.
    """
    username = request.args.get('username')
    if not username:
        return jsonify({"message": "Username is required to fetch user data!"}), 400
    
    # Получаем данные пользователя из кэша
    user_data = cache.get(f"user:{username}")
    
    if user_data:
        # Десериализуем данные из JSON строки
        user_data = json.loads(user_data)
        return jsonify(user_data)
    
    return jsonify({"message": f"User {username} not found in cache!"}), 404


# Кэширование звонка
@app.post("/cache/call")
def cache_call():
    """
    Кэширует данные звонка в Redis.
    Ожидает JSON с ключами:
    - 'username': имя пользователя (обязательно)
    - 'date': дата звонка в ISO 8601 формате (обязательно)
    - 'status': статус звонка (обязательно)

    Сохраняет данные звонка в формате JSON, используя ключ 'call:<username>:<date>'.
    """
    data = request.json
    if not data or 'username' not in data or 'date' not in data or 'status' not in data:
        return jsonify({"message": "Username, date, and status are required!"}), 400
    
    # Сериализуем данные звонка в JSON строку
    call_data = json.dumps(data)
    
    # Сохраняем данные звонка в Redis с уникальным ключом
    cache.set(f"call:{data['username']}:{data['date']}", call_data)
    return jsonify({"message": f"Call data for {data['username']} cached successfully!"}), 201

@app.get("/cache/call")
def get_call_result_from_cache():
    """
    Извлекает данные звонка из Redis по имени пользователя и дате.
    Ожидает параметры 'username' и 'date' в запросе.
    """
    username = request.args.get('username')
    date = request.args.get('date')
    if not username or not date:
        return jsonify({"message": "Username and date are required to fetch call data!"}), 400
    
    # Получаем данные звонка из кэша
    call_data = cache.get(f"call:{username}:{date}")
    
    if call_data:
        # Десериализуем данные из JSON строки
        call_data = json.loads(call_data)
        return jsonify(call_data)
    
    return jsonify({"message": f"Call data for {username} on {date} not found in cache!"}), 404

