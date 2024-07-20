import base64
import os
from PIL import Image
import imagehash
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['image_database']
collection = db['images']

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string

def compute_hash(image_path):
    image = Image.open(image_path)
    hash_value = imagehash.phash(image)
    return str(hash_value)

def is_duplicate(hash_value, image_name, threshold=5):
    for record in collection.find():
        stored_hash = imagehash.hex_to_hash(record['hash'])
        if record['name'] == image_name:
            print(f'Image with name {image_name} already exists in the database.')
            return True
        # if imagehash.hex_to_hash(hash_value) - stored_hash <= threshold:
        #     print(f'Image with similar content already exists in the database.')
        #     return True
    return False

def store_image(image_path):
    image_name = os.path.basename(image_path)
    image_data = image_to_base64(image_path)
    hash_value = compute_hash(image_path)
    
    if not is_duplicate(hash_value, image_name):
        document = {
            "name": image_name,
            "image_data": image_data,
            "hash": hash_value
        }
        collection.insert_one(document)
        print(f'Image {image_name} added to the database.')
    else:
        print(f'Image {image_name} is a duplicate and was not added.')

# Example usage
def process_image_directory(directory_path):
    for filename in os.listdir(directory_path):
        image_path = os.path.join(directory_path, filename)
        if os.path.isfile(image_path):
            store_image(image_path)

# Process a directory containing images
directory_path = 'E:/Project/Image_hash/images/'
process_image_directory(directory_path)
