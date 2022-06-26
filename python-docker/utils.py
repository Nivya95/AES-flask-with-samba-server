import hashlib
import os
import datetime
import pymongo


def get_metadata(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)

    file_hash = hash_md5.hexdigest()
    file_size = os.stat(file_path).st_size
    file_modified_time = os.path.getmtime(file_path)
    return {
        "file_hash": file_hash,
        "file_size": file_size,
        "file_modified_time": datetime.datetime.fromtimestamp(
            file_modified_time)
    }


def write_metadata_in_db(metadata):
    myclient = pymongo.MongoClient("mongodb://mongodb:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb["aes"]

    metadata['record_inserted_time'] =datetime.datetime.now()+ datetime.timedelta(hours=2)
    return mycol.insert_one(metadata)
