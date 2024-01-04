import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, validator
from typing import Optional
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import requests
from pymongo import MongoClient


from driver_selenium.soup_read_file import SoupHtmlFile
from driver_selenium.class_driver import TelegramParser


MONGO_URL='mongodb://mongo:27017/'
client = MongoClient(MONGO_URL)
db = client["telegram"]

def send_telegram_post(type_telegram):
    # Дані для POST-запиту
    data = {
        "typeTelegram": type_telegram,
        "indexStation": "string",
        "numberMessages": "string",
        "dateStartingInput": "string",
        "dateFinishInput": "string",
        "timeStartingInput": "string",
        "timeFinishInput": "string"
    }    
    # Виконання POST-запиту до /telegram
    response = requests.post('http://localhost:8000/selenium_telegram', json=data)
    return response

# Створення планувальника задач
scheduler = BackgroundScheduler()

# Додавання задач до планувальника з використанням CronTrigger
scheduler.add_job(send_telegram_post, args=['meteo'],
                  trigger=CronTrigger(hour='0,3,6,9,12,15,18,21', minute=25, second=0, day_of_week='*'))
scheduler.add_job(send_telegram_post, args=['hydro'], 
                  trigger=CronTrigger(hour=10, minute=30, second=0,
                                      day_of_week='*', timezone=pytz.timezone('Europe/Kiev')))
# Запуск планувальника
scheduler.start()

class TypeTelegram(BaseModel):
    typeTelegram: str
    indexStation: Optional[str] = None
    numberMessages: Optional[str] = None
    dateStartingInput: Optional[str] = None
    dateFinishInput: Optional[str] = None
    timeStartingInput: Optional[str] = None
    timeFinishInput: Optional[str] = None

    @validator('*')
    def check_string_fields(cls, v):
        return None if v == 'string' else v

    @validator('typeTelegram')
    def check_typeTelegram(cls, v):
        allowed_values = ["hydro", "meteo"]
        if v not in allowed_values:
            raise ValueError(f'typeTelegram must be one of {allowed_values}')
        return v
    
class PostTelegrame(BaseModel):
    typeTelegram: Optional[str]
    indexStation: Optional[str]
    date: Optional[str]
    time: Optional[str]



app = FastAPI()

@app.on_event("startup")
async def startup_event():
    TelegramParser.restart_session()

@app.on_event("shutdown")
async def shutdown_event():
    TelegramParser.restart_session()



@app.post("/selenium_telegram")
def my_post_route(type_telegram: TypeTelegram):
    driver = TelegramParser()
    driver(**type_telegram.dict())
    return {"message": "Дані успішно отримані"}


@app.post("/telegram")
def post_data(post_request:PostTelegrame):
    collection_name = post_request.typeTelegram
    index_station = post_request.indexStation
    date = post_request.date
    time = post_request.time
    id_teleg = index_station+date+time
    collection = db[collection_name]
    data = collection.find_one({"id_telegram": id_teleg}, {"_id": False})
    if data is None:
        return {"message": "Дані за цей період відсутні"}
    else:
        data['data'] = str(data['data'])
        return data


@app.get("/telegram/{collection_name}/{id_teleg}")
def get_data_from_collection(collection_name: str, id_teleg: str):
    collection = db[collection_name]
    data = collection.find_one({"id_telegram": id_teleg}, {"_id": False})
    if data is None:
        return {"message": "Дані за цей період відсутні"}
    else:
        data['data'] = str(data['data'])
        return data
    

@app.delete("/telegram/{collection_name}/{id_teleg}")
def delete_data_from_collection(collection_name: str, id_teleg: str):
    collection = db[collection_name]
    result = collection.delete_one({"id_telegram": id_teleg})
    if result.deleted_count == 1:
        return {"message": "Дані успішно видалено"}
    else:
        return {"message": "Дані за цей id не знайдені"}
    

@app.put("/telegram/{collection_name}/{id_teleg}")
def update_data_in_collection(collection_name: str, id_teleg: str, dynamic_updates: dict):
    collection = db[collection_name]
    dynamic_updates = {}
    update_fields = {
    f"data.$[item].{field}": value
    for field, value in dynamic_updates.items()}
    result = collection.update_one(
                       {"id_telegram": id_teleg},
                       {"$set": update_fields})
    
    if result.modified_count == 1:
        return {"message": "Дані успішно оновлено"}
    else:
        return {"message": "Дані за цей id не знайдені"}



@app.get("/")
async def root():
    return {"message": "Hello World"}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, root_path="/", log_level="info")




