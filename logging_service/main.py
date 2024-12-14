from flask import Flask, jsonify, request
import os
import dotenv

app = Flask(__name__)

from models import UserLog,CallLog,start_db,session,datetime

@app.before_request
def create_tables():
    start_db()


# Настройки подключения к базе данных

# Запись лога пользователя
@app.post("/log/user")
def set_log_user():
    """
    Записывает лог действия пользователя в базу данных.
    Ожидает JSON с ключами:
    - 'username': имя пользователя (обязательно)
    - 'action': действие, которое совершил пользователь (обязательно)
    """
    data = request.json
    if not data or 'username' not in data or 'action' not in data:
        return jsonify({"message": "Username and action are required!"}), 400

    # Создаём новый лог для пользователя
    log = UserLog(username=data['username'], action=data['action'])
    session.add(log)
    session.commit()
    return jsonify({"message": f"User log for {data['username']} recorded!"}), 201

# Запись лога звонка
@app.post("/log/call")
def set_log_call():
    """
    Записывает лог звонка в базу данных.
    Ожидает JSON с ключами:
    - 'username': имя пользователя (обязательно)
    - 'call_duration': длительность звонка (обязательно)
    - 'status': статус звонка (обязательно)
    """
    data = request.json
    if not data or 'username' not in data or 'call_duration' not in data or 'status' not in data:
        return jsonify({"message": "Username, call_duration, and status are required!"}), 400

    # Создаём новый лог для звонка
    log = CallLog(username=data['username'], call_duration=data['call_duration'], status=data['status'])
    session.add(log)
    session.commit()
    return jsonify({"message": f"Call log for {data['username']} recorded!"}), 201


# Получение логов звонков за период времени
@app.get("/log/calls/")
def calls():
    """
    Извлекает логи звонков за заданный период времени.
    Ожидает параметры:
    - 'start_date': начало периода (в формате YYYY-MM-DDTHH:MM:SS)
    - 'end_date': конец периода (в формате YYYY-MM-DDTHH:MM:SS)
    """
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date or not end_date:
        return jsonify({"message": "Start date and end date are required!"}), 400

    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
        end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return jsonify({"message": "Invalid date format! Use YYYY-MM-DDTHH:MM:SS."}), 400

    # Используем session.query() для получения данных
    logs = session.query(CallLog).filter(
        CallLog.timestamp >= start_date,
        CallLog.timestamp <= end_date
    ).all()

    if not logs:
        return jsonify({"message": "No logs found for the given period."}), 404

    return jsonify([{
        "username": log.username,
        "call_duration": log.call_duration,
        "status": log.status,
        "timestamp": log.timestamp.strftime("%Y-%m-%dT%H:%M:%S")
    } for log in logs])


# Получение логов пользователей за период времени
@app.get("/log/users/")
def users():
    """
    Извлекает логи действий пользователей за заданный период времени.
    Ожидает параметры:
    - 'start_date': начало периода (в формате YYYY-MM-DDTHH:MM:SS)
    - 'end_date': конец периода (в формате YYYY-MM-DDTHH:MM:SS)
    """
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date or not end_date:
        return jsonify({"message": "Start date and end date are required!"}), 400

    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
        end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return jsonify({"message": "Invalid date format! Use YYYY-MM-DDTHH:MM:SS."}), 400

    logs = session.query(UserLog).filter(
        UserLog.timestamp >= start_date,
        UserLog.timestamp <= end_date
    ).all()

    if not logs:
        return jsonify({"message": "No logs found for the given period."}), 404

    return jsonify([{
        "username": log.username,
        "action": log.action,
        "timestamp": log.timestamp.strftime("%Y-%m-%dT%H:%M:%S")
    } for log in logs])


