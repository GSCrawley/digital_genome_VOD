from flask import Flask, render_template, request, redirect, url_for
import dotenv
import boto3
import os
import logging

dotenv.load_dotenv()

app = Flask(__name__, template_folder='./templates')


s3 = boto3.client('s3',
                  aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                  aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

def generate_s3_presigned_url(bucket_name, object_name, expiration=48000):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    print(response)
    # The response contains the presigned URL
    return response

@app.route('/')
def index():
    # presigned_url = generate_s3_presigned_url('gidvidbucket', 'on-failure...mp4')
    presigned_url = "https://gidvidbucket.s3.amazonaws.com/on-failure...mp4?AWSAccessKeyId=AKIAT4BYMASPNVQ4GRZV&Signature=iMNDFuk4U0PAuh3iYRDnkriwp1M%3D&Expires=1714090711"
    return render_template('index.html', presigned_url=presigned_url)

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
