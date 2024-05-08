from flask import Flask, request, redirect, url_for, jsonify
import dotenv
import boto3
import os
import logging

dotenv.load_dotenv()

app = Flask(__name__)


s3 = boto3.client('s3',
                  aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                  aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

def generate_s3_public_url(bucket_name, object_name):
    """Generate a public URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :return: Public URL as string.
    """

    # Generate a public URL for the S3 object
    public_url = f"https://gidvidbucket.s3.amazonaws.com/the_divine_proportion.mp4"

    print(public_url)
    # The public_url contains the public URL
    return public_url

@app.route('/', methods=['POST'])
def index():
    public_url = generate_s3_public_url('gidvidbucket', 'the_divine_proportion.mp4')
    # send to temp_ui
    return jsonify(public_url)
# from botocore.exceptions import NoCredentialsError

# @app.route('/videos', methods=['GET'])
# def list_videos():
#     s3 = boto3.client('s3')
#     try:
#         response = s3.list_objects(Bucket='gidvidbucket')
#     except NoCredentialsError as e:
#         logging.error(e)
#         return None

#     presigned_urls = []
#     for file in response['Contents']:
#         url = s3.generate_presigned_url('get_object', Params={'Bucket': 'gidvidbucket', 'Key': file['Key']}, ExpiresIn=3600)
#         presigned_urls.append(url)

#     return jsonify(presigned_urls)
# @app.route('/', methods=['POST'])
# def upload_file():
#     file = request.files['file']
#     s3.upload_fileobj(file, 'gidvidbucket', file.filename)
#     return redirect(url_for('index'))
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
