import boto3
import os
from dotenv import load_dotenv

load_dotenv()
bucket_name = "gr15"
ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_ACCESS_KEY")

def connectionS3():
    session_aws = boto3.Session(ACCESS_KEY, SECRET_KEY)
    return session_aws.resource('s3')

def get_file(session_s3):    
    bucket_project = session_s3.Bucket(bucket_name)
    bucket_objects = bucket_project.objects.all()
    for obj in bucket_objects:
        print(obj.key)
    print(bucket_objects)

def save_file(id, photo):
    extension = photo.filename.split(".")[1]
    photo_name = f"{id}.{extension}"
    photo_path = f"/tmp/{photo_name}"
    photo.save(photo_path)
    print("Photo saved")
    return photo_path, photo_name

def upload_file_s3(session_s3, photo_path, photo_name):
    path_photo_local = f"images/{photo_name}"
    session_s3.meta.client.upload_file(photo_path, bucket_name, path_photo_local)
    print("Photo uploaded")
    #s3.upload_file()