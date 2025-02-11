# .env dosyasının içeriği
# MONGO_URI=mongodb://localhost:27017
# DATABASE_NAME=Northwind

import os
from dotenv import load_dotenv
from pymongo import MongoClient


# .env dosyasını yükle
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")


print(MONGO_URI)  # mongodb://localhost:27017
print(DATABASE_NAME)  # Northwind


# MongoDB bağlantısını oluştur
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

# category_colleciton = db["Categories"]
# product_collection = db["Products"]
category_collection = db[os.getenv("COLLECTION_CATEGORY")]
product_collection = db[os.getenv("COLLECTION_PRODUCT")]
