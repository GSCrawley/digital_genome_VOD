from flask import Flask, request, redirect, url_for, jsonify
import dotenv
import boto3
import os
import logging
from botocore.exceptions import NoCredentialsError

dotenv.load_dotenv()

app = Flask(__name__)


s3 = boto3.client('s3',
                  aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                  aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

# def generate_s3_public_url(bucket_name, object_name):
#     """Generate a public URL to share an S3 object

#     :param bucket_name: string
#     :param object_name: string
#     :return: Public URL as string.
#     """

#     # Generate a public URL for the S3 object
#     public_url = f"https://gidvidbucket.s3.amazonaws.com/the_divine_proportion.mp4"

#     print(public_url)
#     # The public_url contains the public URL
#     return public_url

def generate_presigned_urls(bucket_name):
    # Create an S3 client
    s3 = boto3.client('s3')
    
    # Try to fetch the list of objects in the bucket
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
    except NoCredentialsError:
       return "AWS credentials not available", 500

    urls = []
    if 'Contents' in response:
        # Generate a presigned URL for each video file
        for obj in response['Contents']:
            video_url = s3.generate_presigned_url('get_object',
                                                  Params={'Bucket': 'gidvidbucket', 'Key': obj['Key']},
                                                  ExpiresIn=3600)  # URL expires in 1 hour
            urls.append(video_url)
    else: 
        return "No videos found in bucket", 404

    return urls

# def index():
#     public_url = generate_s3_public_url('gidvidbucket', 'the_divine_proportion.mp4')
#     # send to temp_ui
#     return jsonify(public_url)



@app.route('/list_videos', methods=['GET'])
def list_videos():
    bucket_name = 'gidvidbucket'  # Example bucket name
    urls = generate_presigned_urls(bucket_name)
    if isinstance(urls, str):
        # If the function returned a string, it's an error message
        return jsonify({'error': urls}), 500
    return jsonify({'urls': urls})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
