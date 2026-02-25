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
Data class for course.
"""


from dataclasses import dataclass
from typing import Optional


@dataclass
class Course:
    """
    Data class for courses.
    """

    # course_id: str
    title: str
    description: str
    instructor: str
    field: str
    level: str
    language: str
    # createdAt: str
    # updatedAt: str
    thumbnailUrl: str
    uid: str
    ratingsAverage: Optional[float] = None
    ratingsCount: Optional[int] = None
    document_id: str = None
    course_id: str = None

    @staticmethod
    def deserialize(document):
        """
        Helper function for parsing a Firestore document to a Course object.

        Parameters:
           document (DocumentSnapshot): A snapshot of Firestore document.

        Output:
           A Course object.
        """

        data = document.to_dict()
        if data:
            return Course(
                document_id=document.id,
                course_id=document.id,
                title=data.get("title"),
                description=data.get("description"),
                instructor=data.get("instructor"),
                field=data.get("field"),
                level=data.get("level"),
                language=data.get("language"),
                # createdAt=data.get("createdAt"),
                # updatedAt=data.get("updatedAt"),
                thumbnailUrl=data.get("thumbnailUrl"),
                uid=data.get("uid"),
                ratingsAverage=data.get("ratingsAverage"),
                ratingsCount=data.get("ratingsCount"),
            )

        return None
