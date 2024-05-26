# Video Server
from flask import Flask, request, redirect, url_for, jsonify
from dotenv import load_dotenv
import boto3
import os
from botocore.exceptions import NoCredentialsError

load_dotenv()

app = Flask(__name__)

# aws_region = os.getenv('AWS_REGION')
bucket_name = os.getenv('S3_BUCKET_NAME')

def fetch_video_list(bucket_name):
    s3 = boto3.client('s3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

    response = s3.list_objects_v2(Bucket=bucket_name)
    video_list = []

    for obj in response.get('Contents', []):
        video_list.append(obj['Key'])
    
    print(video_list)
    return video_list

@app.route('/videos', methods=['GET'])
def list_videos():
    videos = fetch_video_list(bucket_name) # Function to fetch the list of videos without generating presigned URLs
    return jsonify(videos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)