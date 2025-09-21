from pymongo import ASCENDING, MongoClient
from constants import *

def get_mongo_collection(collection:str):
    """
    Connect to MongoDB and return a collection.
    """
    client = MongoClient()
    db = client[DB_NAME]
    return db[collection]

def save(collection, document) -> int:
    """
    Insert a document into the MongoDB collection.

    Args:
        collection: MongoDB collection instance.
        document (dict): The document to insert.
    """
    
    existing_document = collection.find_one({"_id": document["_id"]})

    if existing_document:
        # Document exists, update it
        collection.update_one(
            {"_id": document["_id"]},
            {"$set": document}
        )
        return document["_id"]
    else:
        result = collection.insert_one(document)
        return result.inserted_id
    
def save_qtable(collection, document) -> int:
    """
    Insert a document into the MongoDB collection.

    Args:
        collection: MongoDB collection instance.
        document (dict): The document to insert.
    """
    
    existing_document = collection.find_one({"state_id": document["state_id"], "qlearning_id": document["qlearning_id"]})

    if existing_document:
        # Document exists, update it
        collection.update_one(
            {"_id": existing_document["_id"]},
            {"$set": document}
        )
        return existing_document["_id"]
    else:
        result = collection.insert_one(document)
        return result.inserted_id
    
    
def save_ql_run(collection, document) -> int:
    """
    Insert a run into the MongoDB collection.

    Args:
        collection: MongoDB collection instance.
        document (dict): The document to insert.
    """
    result = collection.insert_one(document)
    return result.inserted_id

def save_ql_mapping(collection, document) -> int:
    """
    Insert a ql mapping document into the MongoDB collection.

    Args:
        collection: MongoDB collection instance.
        document (dict): The document to insert.
    """
    
    existing_document = collection.find_one({"state_id": document["state_id"], "qlearning_id": document["qlearning_id"]})

    if existing_document:
        # Document exists, update it
        collection.update_one(
            {"_id": existing_document["_id"]},
            {"$set": document}
        )
        return existing_document["_id"]
    else:
        result = collection.insert_one(document)
        return result.inserted_id

def load(collection, document_id):
    """
    Retrieve a document by its ID from the MongoDB collection.

    Args:
        collection: MongoDB collection instance.
        document_id: The ID of the document to retrieve.

    Returns:
        dict: The retrieved document.
    """
    document = collection.find_one({"_id": document_id})
    if document is None:
        print(f"No document found with ID: {document_id}")
    return document

def get_next_id(collection):
    """
    Returns the next ID for a MongoDB collection based on the count of documents.
    
    :param collection: The MongoDB collection object
    :return: The next ID (count + 1)
    """
    count = collection.count_documents({})
    return str(count + 1)


def create_qtable_collection():
    """Create the Q-table collection if it doesn't exist and add an index on qlearning_id and state_id."""
    
    client = MongoClient()
    db = client[DB_NAME]
    
    if DB_COLLECTION_QTABLE not in db.list_collection_names():
        # Create collection with the necessary structure
        collection = db.get_collection(DB_COLLECTION_QTABLE)
        collection.create_index([("qlearning_id", ASCENDING), ("state_id", ASCENDING)], unique=True)
    

test_document = {
    "id": 1,
    "qtable": [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ],
    "mapping": {
        "action1": [[1,2,3],[1,2,3]],
    },
    "epsilon": 3.14
}

# test
""" if __name__ == "__main__":
    collection = get_mongo_collection("test")

    save(collection, test_document)

    retrieved_document = load(collection, 1)
    print("Retrieved Document:")
    print(retrieved_document) """
