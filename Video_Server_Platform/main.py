from flask import Flask, render_template, request, redirect, url_for
import dotenv
import boto3
import os
import logging

dotenv.load_dotenv()

app = Flask(__name__, template_folder='../video_client/templates')


s3 = boto3.client('s3',
                  aws_access_key_id=os.getenv('YOUR_ACCESS_KEY'),
                  aws_secret_access_key=os.getenv('YOUR_SECRET_KEY'))

def generate_s3_presigned_url(bucket_name, object_name, expiration=3600):
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

    # The response contains the presigned URL
    return response
    
@app.route('/')
def index():
    presigned_url = generate_s3_presigned_url('gidvidbucket', 'the_divine_proportion.mp4')
    return render_template('index.html', presigned_url=presigned_url)

# @app.route('/', methods=['POST'])
# def upload_file():
#     file = request.files['file']
#     s3.upload_fileobj(file, 'gidvidbucket', file.filename)
#     return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)