import base64
import imagehash
import time
from PIL import Image
from pymongo import MongoClient

# Initialize MongoDB client and select database and collection
client = MongoClient('mongodb://localhost:27017/')
db = client['image_database']
collection = db['images']

def compute_hash(image_path):
    image = Image.open(image_path)
    hash_value = imagehash.phash(image)
    return str(hash_value)

def is_duplicate(hash_value, threshold=5):
    # Query for similar hashes within a Hamming distance threshold
    for record in collection.find():
        stored_hash = imagehash.hex_to_hash(record['hash'])
        if imagehash.hex_to_hash(hash_value) - stored_hash <= threshold:
            return True
    return False

def add_image(image_path):
    start_time = time.time()
    
    # Compute hash
    hash_start = time.time()
    hash_value = compute_hash(image_path)
    hash_end = time.time()
    
    # Check for duplicates
    duplicate_check_start = time.time()
    if not is_duplicate(hash_value):
        duplicate_check_end = time.time()
        
        # Convert image to base64
        base64_start = time.time()
        image_data = image_to_base64(image_path)
        base64_end = time.time()
        
        # Insert into database
        insert_start = time.time()
        document = {
            'hash': hash_value,
            'image_path': image_path,
            'image_data': image_data
        }
        collection.insert_one(document)
        insert_end = time.time()
        
        end_time = time.time()
        print(f'Image {image_path} added to the database.')
    else:
        duplicate_check_end = time.time()
        end_time = time.time()
        print(f'Image {image_path} is a duplicate and was not added.')
    
    # print(f'Total Time: {(end_time - start_time) * 1000:.4f} ms')
    # print(f'Hash Computation Time: {(hash_end - hash_start) * 1000:.4f} ms')
    print(f'Duplicate Check Time: {(duplicate_check_end - duplicate_check_start) * 1000:.4f} ms')
    if not is_duplicate(hash_value):
        print(f'Base64 Conversion Time: {(base64_end - base64_start) * 1000:.4f} ms')
        print(f'Database Insertion Time: {(insert_end - insert_start) * 1000:.4f} ms')

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string

# Example usage
new_image_path = 'E:/Project/Image_hash/images/1.jpg'
add_image(new_image_path)
