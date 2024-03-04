import pandas as pd
from pymongo import MongoClient
import difflib
from concurrent.futures import ThreadPoolExecutor
import logging
from datetime import datetime

# Define database connection settings as constants
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "hygazete"
COLLECTION_NAME = "2014_ilk_6"
SIMILARITY_THRESHOLD = 50  # Similarity threshold as a percentage
OUTPUT_FILE = "similarity_report_post_2014_first_6.xlsx"  # Name of the Excel file where results will be written

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configure MongoDB client connection
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Function to calculate similarity between two texts
def calculate_similarity(text1, text2):
    return difflib.SequenceMatcher(None, text1, text2).ratio() * 100

# Compare a specific document with others to find similar ones
def find_similar_documents(documents, doc_index):
    similarities = []
    main_doc = documents[doc_index]
    if not isinstance(main_doc['content'], str):
        return similarities

    for comparison_doc in documents[doc_index + 1:]:
        if not isinstance(comparison_doc['content'], str):
            continue

        similarity_score = calculate_similarity(main_doc['content'], comparison_doc['content'])
        if similarity_score >= SIMILARITY_THRESHOLD:
            similarities.append({
                'Main Content DB ID': main_doc['_id'],
                'Similar Content DB ID': comparison_doc['_id'],
                'Main Content ID': main_doc['id'],
                'Similar Content ID': comparison_doc['id'],
                'Main Content URL': main_doc['url'],
                'Similar Content URL': comparison_doc['url'],
                'Similarity Score': similarity_score
            })
    return similarities

# Compare contents and write results to Excel
def compare_documents_and_export_to_excel():
    documents = list(collection.find({}, {'_id': 1, 'content': 1, 'url': 1, 'id': 1}))
    logging.info(f"{len(documents)} doküman veritabanında bulundu, karşılaştırma başlıyor.")

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(find_similar_documents, [documents] * len(documents), range(len(documents))))

    all_similarities = [sim for sublist in results for sim in sublist]

    if all_similarities:
        # Convert results to DataFrame
        df = pd.DataFrame(all_similarities)
        # Sort by similarity score in descending order
        df_sorted = df.sort_values('Similarity Score', ascending=False)
        # Save the sorted DataFrame to Excel
        df_sorted.to_excel(OUTPUT_FILE, index=False)
        logging.info(f"Sonuçlar {OUTPUT_FILE} dosyasına yazıldı.")
    else:
        logging.info("Belirlenen eşik değerin üzerinde benzer doküman bulunamadı.")

if __name__ == "__main__":
    compare_documents_and_export_to_excel()