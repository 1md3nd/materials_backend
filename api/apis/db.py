from pymongo import MongoClient
import pandas as pd 
from mongo_client_local import MongoConnection

db = MongoConnection.get_connection().get_database('materials')

# db.drop_collection('all_materials')
collection = db['all_materials']
df = pd.read_csv('updated_data.csv')

for idx, row in df.iterrows():
    row = row.to_dict()
    collection.insert_one(row)


collection.create_index({'compounds_contain':'text'})

print('Insert completed')