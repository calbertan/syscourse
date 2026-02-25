# Copyright 2018 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Cloud Function for processing uploaded images/pdf.
"""


import os
import uuid

from google.cloud import storage
from wand.image import Image
from flask import jsonify, escape

client = storage.Client()

BUCKET = os.environ.get('GCS_BUCKET')
IMAGE_FILENAME_TEMPLATE = '{}.png'
PDF_FILENAME_TEMPLATE = '{}.pdf'
EXPECTED_WIDTH = 640
EXPECTED_HEIGHT = 640

def upload_image(request):
    # Set up CORS to allow requests from arbitrary origins.
    # See https://cloud.google.com/functions/docs/writing/http#handling_cors_requests
    # for more information.
    # For maxiumum security, set Access-Control-Allow-Origin to the domain
    # of your own.
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Max-Age': '3600'
        }
        return ('', 204, headers)
    
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    file = request.files.get('filepond')
    if not file:
        return ("File is not found in the request.", 400, headers)

    file_content = file.read()
    content_type = file.content_type
    id = uuid.uuid4().hex
    original_filename = escape(file.filename)

    if content_type.startswith('image/'):
        with Image(blob=file_content) as image:
            image.transform(resize="{}x{}>".format(EXPECTED_WIDTH, EXPECTED_HEIGHT))
            image.extent(
                width=EXPECTED_WIDTH,
                height=EXPECTED_HEIGHT,
                x=int((EXPECTED_WIDTH - image.width) / 2),
                y=-int((EXPECTED_HEIGHT - image.height) / 2)            
            )
            converted_content = image.make_blob(format='png')
        filename = IMAGE_FILENAME_TEMPLATE.format(id)
        content_disposition = f'attachment; filename="{original_filename}"'
    elif content_type == 'application/pdf':
        converted_content = file_content
        filename = PDF_FILENAME_TEMPLATE.format(id)
        content_disposition = f'attachment; filename="{original_filename}"'
    else:
        return ("Unsupported file type.", 400, headers)
    

    bucket = client.get_bucket(BUCKET)
    blob = bucket.blob(filename)
    blob.upload_from_string(converted_content, content_type=content_type)
    
    # Set the Content-Disposition header
    blob.content_disposition = content_disposition
    blob.patch()
    
    public_url = f'https://storage.googleapis.com/{BUCKET}/{filename}'

    # Return a JSON response with the resource ID and the public URL of the file
    return jsonify({
        'resource_id': id,
        'url': public_url
    }), 200, headers
