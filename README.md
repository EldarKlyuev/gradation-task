# Gradation Project

Полноценное Django приложение с FastAPI, демонстрирующее все требуемые компоненты из задания.

## 🎯 Реализованные компоненты

### 1. ✅ Собственный декоратор
- **Файл**: `utils/decorators.py`
- **Функция**: `measure_time` - измеряет время выполнения функции
- **Применение**: Используется в Django views для измерения времени выполнения API запросов

### 2. ✅ Собственный контекстный менеджер
- **Файл**: `utils/context_managers.py`
- **Класс**: `FileLogger` - автоматически записывает время открытия/закрытия файла
- **Функции**: Автоматическое логирование времени при работе с файлами

### 3. ✅ Настройка CORS
- **Django**: Настроен в `settings.py` с `django-cors-headers`
- **FastAPI**: Настроен в `fastapi_app/main.py` с `CORSMiddleware`
- **Разрешенные домены**: localhost:3000, localhost:8000

### 4. ✅ Подключение PostgreSQL
- **Настройки**: В `settings.py` с поддержкой переменных окружения
- **Fallback**: SQLite для разработки
- **Docker**: PostgreSQL контейнер в `docker-compose.yml`

### 5. ✅ Django REST Framework
- **API**: Полный CRUD для модели User
- **Эндпоинты**: `/api/users/` - все операции с пользователями
- **Сериализаторы**: Отдельные для создания, обновления и чтения

### 6. ✅ Docker Compose
- **Файл**: `docker-compose.yml`
- **Сервисы**: Django, FastAPI, PostgreSQL, Nginx
- **Сети**: Изолированная сеть для всех сервисов

### 7. ✅ Асинхронные функции
- **FastAPI**: Асинхронные эндпоинты
- **HTTP запросы**: `fetch_external_api` с `httpx`
- **Примеры**: `/external-data`, `/weather/{city}`

## 🚀 Быстрый старт

### Локальная разработка

1. **Активация виртуального окружения**:
```bash
venv\Scripts\activate  # Windows
```

2. **Установка зависимостей**:
```bash
pip install -r requirements.txt
```

3. **Настройка базы данных** (SQLite для разработки):
```bash
set USE_SQLITE=True
python manage.py makemigrations
python manage.py migrate
```

4. **Создание суперпользователя**:
```bash
python manage.py createsuperuser
```

5. **Запуск Django**:
```bash
python manage.py runserver
```

6. **Запуск FastAPI** (в отдельном терминале):
```bash
uvicorn fastapi_app.main:app --reload --port 8001
```

### Тестирование компонентов

Запустите тестовый скрипт для демонстрации декоратора и контекстного менеджера:
```bash
python test_utils.py
```

### Docker Compose

1. **Сборка и запуск всех сервисов**:
```bash
docker-compose up --build
```

2. **Доступные сервисы**:
- Django: http://localhost:8000
- FastAPI: http://localhost:8001
- FastAPI Docs: http://localhost:8001/docs
- Nginx: http://localhost:80

## 📁 Структура проекта

```
gradation-task/
├── api/                          # Django API приложение
│   ├── models.py                 # Модель User
│   ├── serializers.py            # DRF сериализаторы
│   ├── views.py                  # API views с декоратором
│   ├── urls.py                   # API маршруты
│   └── admin.py                  # Django админка
├── fastapi_app/                  # FastAPI приложение
│   └── main.py                   # FastAPI с CORS и асинхронными функциями
├── utils/                        # Утилиты
│   ├── decorators.py             # Декоратор measure_time
│   ├── context_managers.py       # Контекстный менеджер FileLogger
│   └── __init__.py
├── gradation_project/            # Django проект
│   ├── settings.py               # Настройки с PostgreSQL и CORS
│   └── urls.py                   # Главные маршруты
├── docker-compose.yml            # Docker Compose конфигурация
├── Dockerfile.django             # Docker для Django
├── Dockerfile.fastapi            # Docker для FastAPI
├── requirements.txt              # Зависимости Python
├── test_utils.py                 # Тестовый скрипт
└── README.md                     # Документация
```

## 🔧 API Endpoints

### Django REST Framework
- `GET /api/users/` - список пользователей
- `POST /api/users/` - создание пользователя
- `GET /api/users/{id}/` - получение пользователя
- `PUT /api/users/{id}/` - обновление пользователя
- `DELETE /api/users/{id}/` - удаление пользователя
- `GET /api/users/me/` - текущий пользователь
- `POST /api/users/login/` - аутентификация

### FastAPI
- `GET /` - корневой эндпоинт
- `GET /users` - список пользователей
- `POST /users` - создание пользователя
- `GET /users/{user_id}` - получение пользователя
- `PUT /users/{user_id}` - обновление пользователя
- `DELETE /users/{user_id}` - удаление пользователя
- `GET /external-data` - асинхронные HTTP запросы
- `GET /weather/{city}` - погода (демо)
- `GET /health` - проверка здоровья

## 🛠 Технологии

- **Backend**: Django 5.2, FastAPI
- **API**: Django REST Framework
- **База данных**: PostgreSQL, SQLite (fallback)
- **CORS**: django-cors-headers, FastAPI CORS
- **Контейнеризация**: Docker, Docker Compose
- **HTTP клиент**: httpx (асинхронный)
- **Веб-сервер**: Nginx (прокси)

## 📝 Примеры использования

### Декоратор measure_time
```python
from utils.decorators import measure_time

@measure_time
def my_function():
    # Ваш код здесь
    pass
```

### Контекстный менеджер FileLogger
```python
from utils.context_managers import FileLogger

with FileLogger('my_file.txt', 'w') as file:
    file.write('Содержимое файла')
# Автоматически запишет время открытия и закрытия
```

### Асинхронные HTTP запросы
```python
import asyncio
from fastapi_app.main import fetch_external_api

async def get_data():
    result = await fetch_external_api("https://api.example.com/data")
    return result
```

## 🔍 Мониторинг

- **Логи времени**: Автоматически выводятся в консоль
- **Файловые логи**: Создаются при использовании FileLogger
- **Health check**: `/health` эндпоинт в FastAPI
- **Django Admin**: http://localhost:8000/admin/

## 🚨 Примечания

1. Для продакшена измените `SECRET_KEY` в `settings.py`
2. Настройте `ALLOWED_HOSTS` для вашего домена
3. Отключите `DEBUG=True` в продакшене
4. Используйте переменные окружения для чувствительных данных 