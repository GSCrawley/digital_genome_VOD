# Video Client Server
from flask import Flask, Response, request, render_template, jsonify
from dotenv import load_dotenv
import sys
import requests
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import os

load_dotenv()  

app = Flask(__name__)
url_dict = {}  # Initialize the URL dictionary to store video URLs

bucket_name = os.getenv('S3_BUCKET_NAME')

@app.route('/')
def index():
    return "stream working"

def generate_presigned_url(bucket_name, video_key):
    try:
        s3_client = boto3.client('s3',
                            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                            aws_session_token=os.getenv('AWS_SESSION_TOKEN'),
                            region_name=os.getenv('AWS_REGION'))
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': video_key},
            ExpiresIn=14400
        )
        return presigned_url
    except NoCredentialsError:
        print("No AWS credentials found.")
        return None
    except ClientError as e:
        print(f"Client error: {e}")
        return None
    except Exception as e:
        # This will catch any other exceptions that are not specific to AWS
        print(f"Unexpected error: {e}")
        return None

@app.route('/video/<video_key>')
def get_video(video_key):
    presigned_url = generate_presigned_url(bucket_name, video_key) # Function to generate presigned URL for the selected video
    if presigned_url:
        return jsonify({'presigned_url': presigned_url})
    else:
        return jsonify({'error': 'Failed to generate presigned URL'}), 500

# The following route will be used when we add video upload capability:

# @app.route('/receive_video', methods=['POST'])
# def receive_video():
#     if 'video' not in request.files:
#         return jsonify({'error': 'No video file part'}), 400

#     video_file = request.files['video']
    
#     if video_file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400

#     if video_file and allowed_file(video_file.filename):
#         # Here you would typically process the file and then upload it to S3
#         # For example, you could save the file temporarily and then use boto3 to upload
#         # Or you could stream the file directly to S3 without saving it locally

#         # ... (Your S3 upload logic)

#         return jsonify({'message': 'Video successfully received'}), 200
#     else:
#         return jsonify({'error': 'Invalid file type'}), 400

# def allowed_file(filename):
#     # Check if the file has one of the allowed extensions
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Define the set of allowed file extensions (e.g., 'mp4', 'avi', 'mov', etc.)
# ALLOWED_EXTENSIONS = set(['mp4', 'avi', 'mov'])


if __name__ == '__main__':
    port = 5001  # Default port
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    app.run(host='0.0.0.0', port=port)