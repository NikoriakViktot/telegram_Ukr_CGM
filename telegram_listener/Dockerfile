# Базовий образ Python
FROM python:3.10-slim

# Встановлення залежностей
RUN pip install fastapi uvicorn redis

# Копіювання коду додатку в контейнер
COPY . . /app

# Встановлення робочої директорії
WORKDIR /app

