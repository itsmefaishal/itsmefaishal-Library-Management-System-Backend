from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

URI = os.getenv('MONGO_MY_URL')

client = MongoClient(URI)