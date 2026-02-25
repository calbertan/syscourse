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
A collection of helper functions for resource related operations.
"""


import requests
from .data_classes import Resource
import os
BUCKET = os.environ.get('GCS_BUCKET')

# Set the base URL of deployed Cloud Function
CLOUD_FUNCTION_BASE_URL = "https://flask-app-4ohwdfnmma-uc.a.run.app"

def add_resource(resource):
    """
    Helper function for adding a resource. Calls a Cloud Function endpoint.

    Parameters:
       resource (Resource): A Resource object.

    Output:
       The ID of the resource
    """
    url = f"{CLOUD_FUNCTION_BASE_URL}/resources"
    response = requests.post(url, json=resource.__dict__)  # Ensure resource is serializable
    if response.ok:
        return response.json().get("resource_id")  # Ensure the key matches the Cloud Function's response
    else:
        response.raise_for_status()

def get_resource(resource_id):
    """
    Helper function for getting a resource. Calls a Cloud Function endpoint.

    Parameters:
       resource_id (str): The ID of the resource.

    Output:
       A Resource object.
    """
    url = f"{CLOUD_FUNCTION_BASE_URL}/resources/{resource_id}"
    response = requests.get(url)
    if response.ok:
        return Resource(**response.json())
    else:
        response.raise_for_status()

def list_resources():
    """
    Helper function for listing resources. Calls a Cloud Function endpoint.

    Parameters:
       None.

    Output:
       A list of Resource objects.
    """
    url = f"{CLOUD_FUNCTION_BASE_URL}/resources"
    response = requests.get(url)
    if response.ok:
        resources_data = response.json()
        resources = []
        for res in resources_data:
            resource = Resource(
                course_id=res.get('course_id'),
                title=res.get('title'),
                type=res.get('type'),
                url=res.get('url'),
                description=res.get('description'),
                uid=res.get('uid'),
                thumbnail=res.get('thumbnail'),
                duration=res.get('duration'),
                document_id=res.get('document_id'),
                resource_id=res.get('resource_id')
            )
            resources.append(resource)
        return resources
    else:
        response.raise_for_status()

def list_resources_by_course(course_id):
    """
    Helper function for listing resources based on course id. Calls a Cloud Function endpoint.

    Parameters:
       course_id (str): The ID of the course.

    Output:
       A list of Resource objects.
    """
    url = f"{CLOUD_FUNCTION_BASE_URL}/resources/course/{course_id}"
    response = requests.get(url)
    if response.ok:
        resources_data = response.json()
        resources = []
        for res in resources_data:
            resource = Resource(
                course_id=res.get('course_id'),
                title=res.get('title'),
                type=res.get('type'),
                url=res.get('url'),
                description=res.get('description'),
                uid=res.get('uid'),
                thumbnail=res.get('thumbnail'),
                duration=res.get('duration'),
                document_id=res.get('document_id'),
                resource_id=res.get('resource_id')
            )
            resources.append(resource)
        return resources
    else:
        response.raise_for_status()

def delete_resource(uid, resource_id):
    """
    Deletes a resource based on UID and resource ID. Calls a Cloud Function endpoint.

    Parameters:
    - uid (str): The unique ID of the user who owns the resource.
    - resource_id (str): The ID of the resource to be deleted.

    Output:
    - A message indicating the outcome of the operation.
    """
    url = f"{CLOUD_FUNCTION_BASE_URL}/resources/{resource_id}"
    response = requests.delete(url, params={"resource_id": resource_id})
    if response.ok:
        return "Resource successfully deleted."
    else:
        return response.text