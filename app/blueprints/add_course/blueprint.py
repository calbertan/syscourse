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
This module is the Flask blueprint for the add course page (/add_course).
"""


from dataclasses import asdict
import os
import random
import requests

from flask import Blueprint, redirect, render_template, url_for

from helpers import eventing, auth, courses
from middlewares.auth import auth_required
from middlewares.form_validation import AddCourseForm, course_form_validation_required

PUBSUB_TOPIC_NEW_PRODUCT = os.environ.get('PUBSUB_TOPIC_NEW_PRODUCT')
API_GATEWAY = os.environ.get('API_GATEWAY_URL')

add_course_page = Blueprint('add_course_page', __name__)

@add_course_page.route('/add_course', methods=['GET'])
@auth_required
def display(auth_context):
    """
    View function for displaying the add_course page.

    Parameters:
       auth_context (dict): The authentication context of request.
                            See middlewares/auth.py for more information.
    Output:
       Rendered HTML page.
    """

    # Prepares the add_course form.
    # See middlewares/form_validation.py for more information.
    form = AddCourseForm()
    return render_template('add_course.html', auth_context=auth_context, form=form)


@add_course_page.route('/add_course', methods=['POST'])
@auth_required
@course_form_validation_required
def process(auth_context, form):
    """
    View function for processing add_course requests.

    Parameters:
       auth_context (dict): The authentication context of request.
                            See middlewares/auth.py for more information.
       form (AddCourseForm): A validated add_course form.
                             See middlewares/form_validation.py for more
                             information.
    Output:
       Rendered HTML page.
    """
    new_course = courses.Course(
        title=form.title.data,
        description=form.description.data,
        instructor=form.instructor.data,
        field=form.field.data,
        level=form.level.data, 
        language=form.language.data,
        thumbnailUrl="course",  
        uid=auth_context.get("uid"),
        ratingsAverage="{:.1f}".format(random.uniform(1, 4.9)),
        ratingsCount=str(random.randint(1, 1000))
    )
    new_course_dict = asdict(new_course)
    
    api_gateway_url = API_GATEWAY + "/courses"
    jwt_cred = auth.generate_creds(
        sa_keyfile="keyfile.json",
        sa_email=os.environ.get('JWT_EMAIL'),
        audience=API_GATEWAY
    )
    response = auth.make_authorized_post_request(
        jwt_cred,
        url=api_gateway_url,
        data=new_course_dict
    )
    
    if response.ok:
        email = auth_context.get('email')
        eventing.stream_event(
            topic_name=PUBSUB_TOPIC_NEW_PRODUCT,
            event_type='new-product-sub',
            event_context={
                'to': email,
                'subject': 'Successfully Added Course to Syscourse',
                'text': 'course uploaded to syscourse successfully.'
            }
        )
        return redirect(url_for('course_page.display'))
    else:
        # Handle the case where the request to the API Gateway fails
        return "Error: Failed to add course", 500
