from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

class DatabaseManager:
    def __init__(self, db):
        self.db = db

    def get_or_create_collection(self, collection_name):
        if collection_name in self.db.list_collection_names():
            return self.db[collection_name]
        else:
            return self.db.create_collection(collection_name)

    def insert_document_if_not_exists(self, collection, document):
        if not collection.find_one({"id_telegram": document["id_telegram"]}):
            collection.insert_one(document)

    def get_water_level(self, type_telegram, id_telegram):
        collection = self.db[type_telegram]
        doc = collection.find_one({"id_telegram": id_telegram})
        water_level = doc["data"][1]["water_level"]
        return water_level

    def get_telegrams(self, type_telegram, index_station, date):
        collection = self.db[type_telegram]
        docs = collection.find({"index_station": index_station, "date_telegram": date})
        for doc in docs:
            print(doc)  # or do something else with the document
    
    def insert_or_update_document(self, collection, document):
        existing_doc = collection.find_one({"id_telegram": document["id_telegram"]})
        if existing_doc is not None:
            if existing_doc['data'] != document['data']:  # if telegram in the document has been changed
                collection.find_one_and_update(
                    {"id_telegram": document["id_telegram"]},
                    {"$set": {"data": document['data']}}
                )
        else:
            try:
                collection.insert_one(document)
            except DuplicateKeyError:
                print(f"Document with id {document['id_telegram']} already exists.")    



class MongoDb:
    MONGO_URL = 'mongodb://mongo:27017/'

    def __init__(self):
        client = MongoClient(self.MONGO_URL)
        self.db = client["telegram"]
        self.db_manager = DatabaseManager(self.db)

    def save_document(self):
        self.db_manager.insert_document_if_not_exists(collection, document_mongo)

    def get_water_level(self, type_telegram, id_telegram):
        return self.db_manager.get_water_level(type_telegram, id_telegram)

    def get_telegrams(self, type_telegram, index_station, date):
        self.db_manager.get_telegrams(type_telegram, index_station, date)

    

# class MongoDb:
#     MONGO_URL='mongodb://mongo:27017/'
#     client = MongoClient(MONGO_URL)
#     db = client["telegram"]
     
     
#     def __init__(self, type_telegram):
#         self.type_telegram = type_telegram



#     def save_document(self):
#         file_html = SoupHtmlFile()
#         type_telegram = self.type_telegram
#         if type_telegram in self.db.list_collection_names():
#             collection = self.db[type_telegram]
#         else:
#             collection = self.db.create_collection(type_telegram)
#         for report_today in file_html.report():
#             id_teleg = report_today.id_telegrame
#             date_tel = report_today.date_telegram
#             time_teleg = report_today.time_telegram
#             index_post = report_today.index_station
#             text_telegram = report_today.gauges_telegrame 
#             data_telegram = {
#                 "id_teleg": id_teleg,
#                 "date_telegram": date_tel,
#                 "time_telegram": time_teleg,
#                 "index_station": index_post,
#                 "gauges_telegram": text_telegram}
#             if type_telegram == 'hydro':
#                 decode_tel = KC15(data_telegram)
#                 mesured_data = decode_tel.report_dict()
#             else:
#                 mesured_data = None    
#             document_mongo = {
#             "id_telegram": id_teleg,
#             "data": [data_telegram, mesured_data]}
#             get_id = collection.find_one({"id_telegram": id_teleg})
#             if get_id is None:
#                 collection.insert_one(document_mongo)

#     def get_water_level(self, id_telegram):
#         collection = self.db[self.type_telegram]
#         doc = collection.find_one({"id_telegram": id_telegram})
#         water_level = doc["data"][1]["water_level"]
#         return water_level

#     def get_telegrams(self, index_station, date):
#         collection = self.db[self.type_telegram]
#         # Notice that we use find() here instead of find_one()
#         docs = collection.find({"index_station": index_station, "date_telegram": date})
#         for doc in docs:
#             print(doc)  # or do something else with the document
    
            
