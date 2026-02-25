import os
from helpers import auth
from middlewares.auth import auth_required, auth_optional

from flask import Blueprint, render_template

all_course_page = Blueprint('all_course_page', __name__)
API_GATEWAY = os.environ.get('API_GATEWAY_URL')

@all_course_page.route('/all_course')
@auth_optional
def display(auth_context):
    """
    View function for displaying the courses page.
    """
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
    course_items = response.json()
    
    return render_template(
        "all_course_page.html",
        courses=course_items,
        auth_context=auth_context,
        bucket=os.environ.get('GCS_BUCKET'),
    )
