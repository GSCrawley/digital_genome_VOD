# Video_Server
from flask import Flask, request, jsonify, send_file
from dotenv import load_dotenv
import boto3
import os
from botocore.exceptions import NoCredentialsError, ClientError


load_dotenv()

app = Flask(__name__)

aws_region = os.getenv('AWS_REGION')
bucket_name = os.getenv('S3_BUCKET_NAME')

@app.route('/presigned', methods=['POST'])
def generate_presigned_url():
    data = request.get_json()
    video_key = data
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
        return jsonify({'presigned_url': presigned_url})
    except NoCredentialsError:
        print("No AWS credentials found.")
        return jsonify({'error': 'No AWS credentials found'}), 500
    except ClientError as e:
        print(f"Client error: {e}")
        return jsonify({'error': 'Client error occurred'}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({'error': 'Unexpected error occurred'}), 500

def fetch_video_list(bucket_name):
    s3 = boto3.client('s3',
                      aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                      aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

    response = s3.list_objects_v2(Bucket=bucket_name)
    video_list = []

    for obj in response.get('Contents', []):
        key = obj['Key']
        if key.endswith('.mp4'):
            video_name = key[:-4]  # Remove .mp4 extension
            thumbnail = f"{video_name}_thumbnail.png"
            video_list.append({
                'name': video_name,
                'video': key,
                'thumbnail': thumbnail
            })

    print(video_list)
    return video_list

@app.route('/videos', methods=['GET'])
def list_videos():
    videos = fetch_video_list(bucket_name)
    return jsonify(videos)

@app.route('/thumbnail/<path:thumbnail_key>')
def get_thumbnail(thumbnail_key):
    try:
        s3_client = boto3.client('s3',
                                 aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                 aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                                 aws_session_token=os.getenv('AWS_SESSION_TOKEN'),
                                 region_name=os.getenv('AWS_REGION'))

        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': thumbnail_key},
            ExpiresIn=3600
        )
        return jsonify({'presigned_url': presigned_url})
    except Exception as e:
        print(f"Error generating presigned URL for thumbnail: {e}")
        return jsonify({'error': 'Failed to generate presigned URL for thumbnail'}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)
