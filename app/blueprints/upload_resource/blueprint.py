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
This module is the Flask blueprint for the upload resource page (/upload_resource).
"""


from dataclasses import asdict
import os
import requests

from flask import Blueprint, redirect, render_template, url_for, request, current_app, flash
from werkzeug.utils import secure_filename


from helpers import eventing, auth, resources
from middlewares.auth import auth_required
from middlewares.form_validation import (
    ResourceUploadForm,
    resource_form_validation_required,
)

PUBSUB_TOPIC_NEW_PRODUCT = os.environ.get('PUBSUB_TOPIC_NEW_PRODUCT')
API_GATEWAY = os.environ.get('API_GATEWAY_URL')

upload_resource_page = Blueprint("upload_resource_page", __name__)


@upload_resource_page.route("/upload_resource", methods=["GET"])
@auth_required
def display(auth_context):
    """
    View function for displaying the upload resource page.

    Parameters:
       auth_context (dict): The authentication context of request.
                            See middlewares/auth.py for more information.
    Output:
       Rendered HTML page.
    """

    # Prepares the upload resourse form.
    # See middlewares/form_validation.py for more information.
    api_gateway_url = API_GATEWAY + "/courses"
    jwt_cred = auth.generate_creds(
        sa_keyfile="keyfile.json",
        sa_email=os.environ.get('JWT_EMAIL'),
        audience=API_GATEWAY
    )
    response = auth.make_authorized_get_request(
        jwt_cred,
        url=api_gateway_url
    )
    list_course = response.json()
    
    form = ResourceUploadForm()
    form.course_id.choices = [
        (course["course_id"], course["title"]) for course in list_course
    ]
    return render_template("upload_resource.html", auth_context=auth_context, form=form)


@upload_resource_page.route("/upload_resource", methods=["POST"])
@auth_required
@resource_form_validation_required
def process(auth_context, form):
    """
    View function for processing upload resource requests.

    Parameters:
       auth_context (dict): The authentication context of request.
                            See middlewares/auth.py for more information.
       form (SellForm): A validated upload_resource form.
                        See middlewares/form_validation.py for more
                        information.
    Output:
       Rendered HTML page.
    """
    jwt_cred = auth.generate_creds(
        sa_keyfile="keyfile.json",
        sa_email=os.environ.get('JWT_EMAIL'),
        audience=API_GATEWAY
    )
    
    file = request.files.get('resourceFile')
    if not file or file.filename == '':
        # Flash message and redirect if no file is selected
        flash('No file selected for uploading', 'error')
        return redirect(url_for("upload_resource_page.display", _anchor='form'))
    
    # Continue processing since there is a file
    filename = secure_filename(file.filename)
    files = {'filepond': (filename, file, file.content_type)}
    
    # Send the file to the Cloud Function
    api_gateway_url = API_GATEWAY + "/upload_image"
    response = auth.make_authorized_post_files_request(
        jwt_cred,
        url=api_gateway_url,
        files=files
    )
    if response.status_code != 200:
        # Flash message and redirect if cloud function fails
        flash('Error uploading file', 'error')
        return redirect(url_for("upload_resource_page.display", _anchor='form'))
    
    # If the request was successful, extract the response data
    response_data = response.json()
     
    # get list of courses
    api_gateway_url = API_GATEWAY + "/courses"
    response = auth.make_authorized_get_request(
        jwt_cred,
        url=api_gateway_url
    )
    list_course = response.json()
    
    form.course_id.choices = [
        (course["course_id"], course["title"]) for course in list_course
    ]
    
    # Create the Resource object with the data from the response
    upload_resource = resources.Resource(
        title=form.title.data,
        description=form.description.data,
        url=response_data.get('url'), # URL from the Cloud Function response
        type=file.content_type,    # MIME type of the file
        uid=auth_context.get("uid"),
        thumbnail="resource_1",
        course_id=form.course_id.data,
        resource_id=response_data.get('resource_id')  # Resource ID from the response
    )

    new_upload_resource = asdict(upload_resource)
    
    api_gateway_url = API_GATEWAY + "/resources"
    response = auth.make_authorized_post_request(
        jwt_cred,
        url=api_gateway_url,
        data=new_upload_resource
    )
    
    if response.ok:
        email = auth_context.get('email')
        eventing.stream_event(
            topic_name=PUBSUB_TOPIC_NEW_PRODUCT,
            event_type='new-product-sub',
            event_context={
                'to': email,
                'subject': 'Successfully Uploaded Resource to Syscourse',
                'text': 'resource uploaded to syscourse.'
            }
        )
        return redirect(url_for("course_page.display"))
    else:
        # Handle the case where the request to the API Gateway fails
        return "Error: Failed to add course", 500
