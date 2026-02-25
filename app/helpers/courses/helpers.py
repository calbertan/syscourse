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
A collection of helper functions for courses related operations.
"""

import os

import requests
from .data_classes import Course

BUCKET = os.environ.get("GCS_BUCKET")


# Set the base URL of deployed Cloud Function
CLOUD_FUNCTION_BASE_URL = "https://course-helper-ayc2jvsxua-uc.a.run.app"


def add_course(course):
    """
    Helper function for adding a course.

    Parameters:
       course (Course): A Course object.

    Output:
       The ID of the course.
    """
    url = f"{CLOUD_FUNCTION_BASE_URL}/courses"
    response = requests.post(
        url, json=course.__dict__
    )  # Ensure resource is serializable
    if response.ok:
        return response.json().get(
            "course_id"
        )  # Ensure the key matches the Cloud Function's response
    else:
        response.raise_for_status()


def get_course(course_id):
    """
    Helper function for getting a course.

    Parameters:
       course_id (str): The unique ID of a course.

    Output:
       A Course Object.
    """

    url = f"{CLOUD_FUNCTION_BASE_URL}/courses/{course_id}"
    response = requests.get(url)
    if response.ok:
        return Course(**response.json())
    else:
        response.raise_for_status()


def list_course():
    """
    Helper function for listing courses base on ratings

    Parameters:
       None.

    Output:
       A list of Course objects.
    """
    #  courses = firestore_client.collection("courses").order_by("ratingsAverage").get()
    #  course_list = [Course.deserialize(course) for course in list(courses)]
    #  course_list.sort(key=lambda x: (x.ratingsAverage, x.ratingsCount))
    #  return course_list
    url = f"{CLOUD_FUNCTION_BASE_URL}/courses"
    response = requests.get(url)
    if response.ok:
        courses_data = response.json()
        courses = []
        for res in courses_data:
            course = Course(
                course_id=res.get("course_id"),
                title=res.get("title"),
                instructor=res.get("instructor"),
                field=res.get("field"),
                level=res.get("level"),
                language=res.get("language"),
                thumbnailUrl=res.get("thumbnailUrl"),
                description=res.get("description"),
                uid=res.get("uid"),
                ratingsAverage=res.get("ratingsAverage"),
                ratingsCount=res.get("ratingsCount"),
                document_id=res.get("document_id"),
            )
            courses.append(course)
        return courses
    else:
        response.raise_for_status()



def remove_course(uid, course_id):
    """
    Helper function for deleting a course based on user ID and course ID.

    Parameters:
       uid (str): The unique ID of a user.
       course_id (str): The ID of the course to be deleted.

    Output:
       A message indicating whether the course was successfully deleted or not.
    """
    # Reference to the specific course document
    url = f"{CLOUD_FUNCTION_BASE_URL}/courses/{course_id}/{uid}"
    response = requests.delete(url, params={"course_id": course_id, "uid": uid})
    if response.ok:
        return "Resource successfully deleted."
    else:
        return response.text
