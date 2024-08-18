# Duplicated Image Check

## About The Project

Two Python Scripts : one for storing images to MongoDB, one for checking duplicated image.

We calculate hash for every image and store image and its hash to MongoDB.

For new image, we calculate its hash and check if there is same hash within Database.

If there is, we don't store it.

## How to run this project

```bash
pip install pymongo
```