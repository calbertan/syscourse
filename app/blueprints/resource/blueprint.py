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
This module is the Flask blueprint for the resource page (/resource).
"""

import requests
import os
from flask import Blueprint, render_template, request

from helpers import auth, resources
from middlewares.auth import auth_required, auth_optional


resource_page = Blueprint("resource_page", __name__)
API_GATEWAY = os.environ.get('API_GATEWAY_URL')

@resource_page.route('/resource', methods=['GET'])
@auth_required
def display_specific(auth_context):
    """
    View function for displaying the specifications of the course.

    Parameters:
        auth_context (dict): The authentication context of request.
                             See middlewares/auth.py for more information.
    Output:
        Rendered HTML page.
    """

    resource_id = request.args.get('resource_id')    
    
    if resource_id:
        # Fetch course details based on course_id
        api_gateway_url = API_GATEWAY + "/resources/" + resource_id
        jwt_cred = auth.generate_creds(
            sa_keyfile="keyfile.json",
            sa_email=os.environ.get('JWT_EMAIL'),
            audience=API_GATEWAY
        )
        response = auth.make_authorized_get_request(
            jwt_cred,
            url=api_gateway_url,
        )
        resource = response.json()
        return render_template('resource.html', resource=resource, auth_context=auth_context, bucket=resources.BUCKET)
    else:
        return "Course ID is required", 400


@resource_page.route("/resource", methods=["DELETE"])
@auth_required
def remove(auth_context):
    """
    Endpoint for removing an item from cart.

    Parameters:
       auth_context (dict): The authentication context of request.
                            See middlewares/auth.py for more information.
    Output:
       Text message with HTTP status code 200.
    """
    ## need to be implemented
