import os
import boto3
from flask import current_app

local_storage_folder_name = "Uploads"

def upload_file(file):
    if current_app.config["STORAGE_MODE"] == "local":
        os.makedirs(local_storage_folder_name, exist_ok = True)
        path = os.path.join(local_storage_folder_name, file.filename)
        file.save(path)
        return path

def delete_file(filename):
    if current_app.config["STORAGE_MODE"] == "local":
        path = os.path.join(local_storage_folder_name, filename)
        if os.path.exists(path):
            os.remove(path)