from pymongo import MongoClient

client = MongoClient("mongodb+srv://Tanoshi:nathaniel111@eventlink.1hfcs.mongodb.net/")
db = client["EventLink"]

# List all collections you want to clear
collections = ["users", "regions", "events", "notifications"]

for collection_name in collections:
    collection = db[collection_name]
    result = collection.delete_many({})
    print(f"Deleted {result.deleted_count} documents from {collection_name} collection.")
