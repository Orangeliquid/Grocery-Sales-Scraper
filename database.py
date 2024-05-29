from pymongo import MongoClient, errors
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Connect to MongoDB
try:
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
    db = client["Grocery_Sales"]
    # Trigger a server selection to test the connection
    client.server_info()
    logging.info("Successfully connected to MongoDB")
except errors.ServerSelectionTimeoutError as e:
    logging.error(f"Error connecting to MongoDB: {e}")
    raise


def store_in_database(product_name, product_data):
    collection = db.get_collection(product_name)
    current_date = datetime.combine(datetime.utcnow().date(), datetime.min.time())

    # Check if there is already data for the current date
    existing_data = collection.find_one({"date": current_date})

    if existing_data:
        logging.info(
            f"Data already found in MongoDB for: {product_name} Date: {current_date}\n Collection not updated.")
    else:
        collection.insert_one({
            "date": current_date,
            "product_data": product_data
        })
        logging.info(f"Stored new data for {product_name} on {current_date} in MongoDB")


def get_product_data(product_name):
    collection = db.get_collection(product_name)

    # Check if collection is empty
    if collection.count_documents({}) == 0:
        return f"Nothing found for '{product_name}'. Please check spelling or database for existence."

    all_documents = collection.find()

    try:
        for document in all_documents:
            print(document)
        return f"All documents printed for '{product_name}'"
    except Exception as e:
        logging.error(f"An error occurred while fetching documents: {e}")
        return "An error occurred while fetching documents."


def get_all_logged_products():
    return db.list_collection_names()


if __name__ == '__main__':
    pass
