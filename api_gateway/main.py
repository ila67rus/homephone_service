from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import httpx
import os
import dotenv

dotenv.load_dotenv()

app = FastAPI()

# Адреса сервисов
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")
CALL_SERVICE_URL = os.getenv("CALL_SERVICE_URL")
LOGGING_SERVICE_URL = os.getenv("LOGGING_SERVICE_URL")
CALLCACHE_SERVICE_URL = os.getenv("CALLCACHE_SERVICE_URL") 

# Модель для данных пользователя
class User(BaseModel):
    name: str
    phone: str




@app.get("/")
async def user_service_home():
    """Главная страница User Service через API Gateway"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USER_SERVICE_URL}/")
        if response.status_code == 200:
            return response.text  # Возвращаем текстовое содержимое
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)


@app.post("/users/")
async def create_user(user: User):
    """Создать нового пользователя через User Service и записать лог через Logging Service"""
    async with httpx.AsyncClient() as client:
        # Шаг 1: Создать пользователя через User Service
        response = await client.post(f"{USER_SERVICE_URL}/users/", json=user.model_dump())
        
        if response.status_code == 201:
            user_response = response.json()

            # Шаг 2: Создать лог для пользователя через Logging Service
            log_data = {
                "username": user_response.get('name', user.name),  # Используем имя из ответа или переданного объекта
                "action": "User created"
            }
            
            log_response = await client.post(f"{LOGGING_SERVICE_URL}/log/user", json=log_data)
            
            if log_response.status_code == 201:
                return {"message": "User created and logged successfully", "user": user_response}
            else:
                raise HTTPException(status_code=log_response.status_code, detail="Failed to log the user creation")
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        
@app.get("/users/")
async def users():
    """Получить информацию о пользователях через User Service"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USER_SERVICE_URL}/users/")
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """Получить информацию о пользователе по ID через User Service"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USER_SERVICE_URL}/users/{user_id}")
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

@app.delete("/users/{user_id}")
async def remove_user(user_id: int):
    """Удалить пользователя через User Service"""
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{USER_SERVICE_URL}/users/{user_id}")
        if response.status_code == 200:
            return {"message": "User deleted successfully."}
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="User not found!")
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

@app.post("/calls/")
async def make_call(request: Request):
    """Инициировать звонок через Call Service и создать лог через Logging Service"""
    call_data = await request.json()

    # Шаг 1: Отправка запроса в Call Service
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{CALL_SERVICE_URL}/call/", json=call_data)
        
        if response.status_code == 201:
            # Шаг 2: Создание лога звонка через Logging Service
            call_response = response.json()
            log_data = {
                "username": call_response['username'],
                "call_duration": 0,  # Задайте подходящее значение
                "status": call_response['status']
            }

            log_response = await client.post(f"{LOGGING_SERVICE_URL}/log/call", json=log_data)
            
            if log_response.status_code == 201:
                return {"message": "Call created and logged successfully", "call": call_response}
            else:
                raise HTTPException(status_code=log_response.status_code, detail="Failed to log the call")
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/calls/history/")
async def get_call_history():
    """Получить историю звонков через Call Service"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CALL_SERVICE_URL}/call/history/")
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)


@app.get("/calls/history/last/")
async def get_last_call():
    """Получить последний звонок через Call Service"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CALL_SERVICE_URL}/call/history/last/")
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/logs/calls/")
async def get_call_logs(start_date: str, end_date: str):
    """Получить логи звонков за период времени через Logging Service"""
    # Формируем параметры запроса
    params = {'start_date': start_date, 'end_date': end_date}
    
    # Отправляем запрос в Logging Service
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{LOGGING_SERVICE_URL}/log/calls/", params=params)
        
        if response.status_code == 200:
            return response.json()  # Возвращаем логи звонков
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/logs/users/")
async def get_user_logs(start_date: str, end_date: str):
    """Получить логи звонков за период времени через Logging Service"""
    # Формируем параметры запроса
    params = {'start_date': start_date, 'end_date': end_date}
    
    # Отправляем запрос в Logging Service
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{LOGGING_SERVICE_URL}/log/users/", params=params)
        
        if response.status_code == 200:
            return response.json()  # Возвращаем логи звонков
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        

