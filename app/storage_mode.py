import os
import boto3
from flask import current_app

local_storage_folder_name = "uploads"

# TODO: Raise exceptinos for any other storage mode that is not local nor s3

def upload_file(file):
    if current_app.config["STORAGE_MODE"] == "local":
        os.makedirs(local_storage_folder_name, exist_ok = True)
        path = os.path.join(local_storage_folder_name, file.filename)
        file.save(path)
        return path
    
    elif current_app.config["STORAGE_MODE"] == "s3":
        s3 = boto3.client(
            "s3",
            aws_access_key_id=current_app.config["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=current_app.config["AWS_SECRET_ACCESS_KEY"],
            region_name=current_app.config["AWS_REGION"],
        )

        s3.upload_fileobj(
            file,
            current_app.config["AWS_BUCKET"],
            file.filename
        )

        return f"https://{current_app.config['AWS_BUCKET']}.s3.amazonaws.com/{file.filename}"

def delete_file(filename):
    if current_app.config["STORAGE_MODE"] == "local":
        path = os.path.join(local_storage_folder_name, filename)
        if os.path.exists(path):
            os.remove(path)

    elif current_app.config["STORAGE_MODE"] == "s3":
        s3 = boto3.client(
            "s3",
            aws_access_key_id=current_app.config["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=current_app.config["AWS_SECRET_ACCESS_KEY"],
            region_name=current_app.config["AWS_REGION"],
        )
        s3.delete_object(
            Bucket=current_app.config["AWS_BUCKET"],
            Key=filename
        )