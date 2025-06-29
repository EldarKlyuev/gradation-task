from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import httpx
import asyncio
from datetime import datetime
import json

app = FastAPI(
    title="Gradation FastAPI",
    description="FastAPI приложение для демонстрации асинхронных функций и CORS",
    version="1.0.0"
)

# CORS настройки - разрешаем только определенные домены
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React frontend
        "http://127.0.0.1:3000",
        "http://localhost:8000",  # Django backend
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Pydantic модели
class User(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None

class UserCreate(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

# Имитация базы данных
users_db = []
user_id_counter = 1

@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {"message": "Добро пожаловать в Gradation FastAPI!"}

@app.get("/users", response_model=List[User])
async def get_users():
    """Получить список всех пользователей"""
    return users_db

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Получить пользователя по ID"""
    for user in users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="Пользователь не найден")

@app.post("/users", response_model=User)
async def create_user(user: UserCreate):
    """Создать нового пользователя"""
    global user_id_counter
    
    # Проверка на существование пользователя
    for existing_user in users_db:
        if existing_user["username"] == user.username or existing_user["email"] == user.email:
            raise HTTPException(status_code=400, detail="Пользователь уже существует")
    
    new_user = User(
        id=user_id_counter,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        created_at=datetime.now()
    )
    
    users_db.append(new_user.dict())
    user_id_counter += 1
    
    return new_user

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserCreate):
    """Обновить пользователя"""
    for i, user in enumerate(users_db):
        if user["id"] == user_id:
            users_db[i].update({
                "username": user_update.username,
                "email": user_update.email,
                "full_name": user_update.full_name
            })
            return users_db[i]
    raise HTTPException(status_code=404, detail="Пользователь не найден")

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    """Удалить пользователя"""
    for i, user in enumerate(users_db):
        if user["id"] == user_id:
            deleted_user = users_db.pop(i)
            return {"message": f"Пользователь {deleted_user['username']} удален"}
    raise HTTPException(status_code=404, detail="Пользователь не найден")

# Асинхронные функции для работы с внешними API
async def fetch_external_api(url: str) -> dict:
    """
    Асинхронная функция для выполнения HTTP-запросов к внешним API
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Ошибка запроса: {str(e)}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"HTTP ошибка: {str(e)}")

@app.get("/external-data")
async def get_external_data():
    """
    Эндпоинт для демонстрации асинхронных HTTP-запросов
    """
    # Выполняем несколько асинхронных запросов одновременно
    tasks = [
        fetch_external_api("https://jsonplaceholder.typicode.com/posts/1"),
        fetch_external_api("https://jsonplaceholder.typicode.com/users/1"),
        fetch_external_api("https://jsonplaceholder.typicode.com/comments/1")
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    return {
        "post": results[0] if not isinstance(results[0], Exception) else {"error": str(results[0])},
        "user": results[1] if not isinstance(results[1], Exception) else {"error": str(results[1])},
        "comment": results[2] if not isinstance(results[2], Exception) else {"error": str(results[2])}
    }

@app.get("/weather/{city}")
async def get_weather(city: str):
    """
    Эндпоинт для получения погоды (демонстрация асинхронного запроса)
    """
    # Имитация запроса к API погоды
    weather_data = await fetch_external_api(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=demo")
    return {"city": city, "weather": weather_data}

@app.get("/health")
async def health_check():
    """Проверка здоровья приложения"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "users_count": len(users_db)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 