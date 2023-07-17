from fastapi import FastAPI
import redis
import uvicorn
import json
app = FastAPI()
redis_url = "redis://redis:6379/0"
 
redis_client = redis.Redis.from_url(redis_url, decode_responses=True)

# Функція, яка обробляє отримані повідомлення
def handle_message(message):
    # Розкодуйте дані та збережіть їх у базі даних PostgreSQL
    # Додайте свою логіку тут
    print("Отримано повідомлення:", message)

# Оголошення маршруту, який буде слухати повідомлення з Redis
def listen_redis():
    channel = redis_client.pubsub()
    channel.subscribe('hydro')

    for message in channel.listen():
       if message["type"] == "message":
           data = json.loads(message["data"])
           print("Прийнято нове повідомлення з Redis:", data)
           handle_message(data)
#


# def startup_event():
#     while True:
#         listen_redis()

if __name__ == "__main__":
    listen_redis()
    