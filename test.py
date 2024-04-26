"""
SENG 533 Final Project
Performance Evaluation of a MongoDB Database
Group 6
"""

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from generate_doc import generate_random_document, generate_update_data, random_document
import time, json, threading

uri = "" # insert real uri to connect to database (in d2l submission comments)
client = MongoClient(uri, server_api=ServerApi('1'))
database = client['sample_airbnb'] # connect to sample_airbnb database
collection = database['listingsAndReviews'] 

#Write-Operations (Inserts, Updates, Deletes) 
# tests inserting documents into collection
def insert_documents(collection, docs):
    documents = [generate_random_document() for _ in range(docs)]
    start_time = time.time()
    result = collection.insert_many(documents)
    end_time = time.time()
    print(f"Insert operation for {docs} documents took {end_time - start_time:.2f} seconds")
    return result.inserted_ids

# tests updating documents in a collection
def update_documents(collection, inserted_ids):
    start_time = time.time()
    for doc_id in inserted_ids:
        updated_data = generate_update_data()
        collection.update_one({'_id': doc_id}, {'$set': updated_data})
    end_time = time.time()
    print(f"Update operation for {len(inserted_ids)} documents took {end_time - start_time:.2f} seconds")

# Comparing Deleting via Indexing
# tests deleting using _id value which has indexing 
def delete_documents(collection, delete): 
    start_time = time.time()
    delete_doc = {"_id": {"$in": delete}}
    result = collection.delete_many(delete_doc)
    end_time = time.time()
    print(f"Delete operation for {result.deleted_count} documents took {end_time - start_time:.2f} seconds") # should be very fast due to indexing on _id

# tests deleting using number of beds (no indexing)
def delete_documents_no_indexing(collection, bed_count): 
    start_time = time.time()
    delete_doc = {"bedrooms": bed_count}
    result = collection.delete_many(delete_doc)
    end_time = time.time()
    print(f"Delete operation for {result.deleted_count} documents took {end_time - start_time:.2f} seconds.")

# tests exporting collections to a file
def export_collection(collection, query={}, file_path='export.json', limit=100): # limit value is how many queries to get from collection, change it to test and collect different amounts
    start_time = time.time()
    if limit:
        data = list(collection.find(query).limit(limit)) 
    else:
        data = list(collection.find(query))
    end_time = time.time()
    print(f"Query operation for {limit} documents took {end_time - start_time:.2f} seconds")

    with open(file_path, 'w') as file:
        json.dump(data, file, default=str) 

    print(f"Data exported to {file_path}")

# test aggregation types (count, distinct, pipeline)
def single_aggregation(collection, min, max):
    start_time = time.time()
    count = collection.count_documents({"price": {"$gte": min, "$lte": max}})
    end_time = time.time()
    print(f"Counting {count} documents with prices between ${min} and ${max} took {end_time - start_time:.2f} seconds")

def distinct_aggregation(collection):
    start_time = time.time()
    amenities = collection.distinct("amenities")
    end_time = time.time()
    print(f"Finding distinct amenities took {end_time - start_time:.2f} seconds")

def aggregation_pipeline(collection):
    start_time = time.time()
    pipeline = [
        {"$match": {"neighborhood_overview": "Greenpoint"}},  # Filter documents from a specific neighborhood
        {"$group": {"_id": "$bedrooms", "average_price": {"$avg": "$price"}}},  # Group by bedrooms and calculate average price
        {"$sort": {"average_price": -1}}  # Sort by average price in descending order
    ]
    results = collection.aggregate(pipeline)
    end_time = time.time()
    print(f"Aggregation pipeline operation took {end_time - start_time:.2f} seconds")

# test average number of documents found per query, total documents found, and how many queries are performed under different workloads
def test_workload(collection, seconds, min_price, max_price):
    end_time = time.time() + seconds
    queries_performed = 0
    total_documents_found = 0

    while time.time() < end_time:
        count = collection.count_documents({"price": {"$gte": min_price, "$lte": max_price}})
        total_documents_found += count  # Sum the documents found in each query
        queries_performed += 1

    average_documents_found = total_documents_found / queries_performed if queries_performed else 0

    print(f"Average number of documents found per query: {average_documents_found:.2f}")
    print(f"Total documents found: {total_documents_found}")
    print(f"Performed {queries_performed} queries in {seconds} seconds.")

# threads via concurrency
def run_threads(collection, num_threads, operation):
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=operation, args=(collection,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

for thread_count in [1, 5]: # can add more threads here
    print(f"Testing with {thread_count} threads.")
    start_time = time.time()
    run_threads(collection, thread_count, random_document)
    end_time = time.time()
    print(f"Concurrency test with {thread_count} threads took {end_time - start_time:.2f} seconds.")

try:
    inserted_ids = insert_documents(collection, 20) 
    update_documents(collection, inserted_ids) 
    export_collection(collection) 
    delete_documents(collection, inserted_ids) # comment out if running delete with no indexing
    # delete_documents_no_indexing(collection, 2) 
    single_aggregation(collection, 5, 100) 
    distinct_aggregation(collection)
    aggregation_pipeline(collection)
    test_workload(collection, 1, 5, 100) # currently tests query performance under 1 second workload
except Exception as e:
    print(e)


