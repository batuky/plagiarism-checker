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
    for subdir, dirs, files in os.walk(directory):
        for json_file in files:
            if json_file.endswith('.json'):
                file_path = os.path.join(subdir, json_file)
                data = load_json_data(file_path)
                insert_data_to_collection(collection, data)
                print(f"{json_file} dosyasındaki veriler MongoDB'ye aktarıldı.")

def main():

    host = 'localhost'
    port = 27017
    database_name = 'hygazete'
    directory = './seperated_posts'

    # Prepare MongoDB client and database
    client = create_mongo_client(host, port)
    db = get_database(client, database_name)

    # Loop through year folders and upload each to MongoDB
    for year in range(2014, 2024 + 1):
        for period in ['ilk 6', 'son 6']:
            collection_name = f"{year} {period}"
            # Create a suitable collection name in the database, for example: "2014 first_6"
            collection = get_collection(db, collection_name.replace(' ', '_'))
            
            # Construct the file path according to the year and period
            year_period_directory = os.path.join(directory, f"{year} {period}")
            if os.path.exists(year_period_directory):
                # Upload JSON files to MongoDB
                upload_json_files_to_mongodb(year_period_directory, collection)

    print("Tüm veriler MongoDB'ye başarıyla aktarıldı.")

if __name__ == "__main__":
    main()