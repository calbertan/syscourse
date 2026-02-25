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
Data class for resource.
"""


from dataclasses import dataclass
from typing import Optional


@dataclass
class Resource:
    """
    Data class for courses.
    """

    resource_id: str
    course_id: str
    title: str
    type: str
    url: str
    description: str
    # createdAt: str
    # updatedAt: str
    thumbnail: str
    uid: str
    duration: Optional[int] = None
    document_id: str = None
    # resource_id: str = None

    @staticmethod
    def deserialize(document):
        """
        Helper function for parsing a Firestore document to a Resource object.

        Parameters:
           document (DocumentSnapshot): A snapshot of Firestore document.

        Output:
           A Resource object.
        """

        data = document.to_dict()
        if data:
            return Resource(
                document_id=document.id,
                resource_id=document.id,
                course_id=data.get("course_id"),
                title=data.get("title"),
                type=data.get("type"),
                url=data.get("url"),
                description=data.get("description"),
                # createdAt=data.get("createdAt"),
                # updatedAt=data.get("updatedAt"),
                thumbnail=data.get("thumbnail"),
                uid=data.get("uid"),
                duration=data.get("duration"),
            )

        return None
