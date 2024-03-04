import pymongo
import json
import os

def create_mongo_client(host, port):
    """Creates and returns a MongoDB client."""
    return pymongo.MongoClient(f"mongodb://{host}:{port}/")

def get_database(client, database_name):
    """Returns a database from the given MongoDB client."""
    return client[database_name]

def get_collection(database, collection_name):
    """Returns a collection from the database."""
    return database[collection_name]

def load_json_data(file_path):
    """Loads and returns JSON data from a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def insert_data_to_collection(collection, data):
    """Inserts the given data into a MongoDB collection."""
    if isinstance(data, list):
        collection.insert_many(data)
    else:
        collection.insert_one(data)

def upload_json_files_to_mongodb(directory, collection):
    """Uploads all JSON files from the specified directory to the MongoDB collection."""
    for json_file in os.listdir(directory):
        if json_file.endswith('.json'):
            file_path = os.path.join(directory, json_file)
            data = load_json_data(file_path)
            insert_data_to_collection(collection, data)
            print(f"{json_file} dosyasındaki veriler MongoDB'ye aktarıldı.")

def main():
    host = 'localhost'
    port = 27017
    database_name = 'hygazete'
    """collection_name options are article, photo-post, post, video-post """
    collection_name = 'video-post'
    directory = 'processed_datas/cleaned_data_video-post_processed'

    # Prepare MongoDB client and collection
    client = create_mongo_client(host, port)
    db = get_database(client, database_name)
    collection = get_collection(db, collection_name)

    # Load JSON files to MongoDB
    upload_json_files_to_mongodb(directory, collection)

    print("Tüm veriler MongoDB'ye başarıyla aktarıldı.")

if __name__ == "__main__":
    main()