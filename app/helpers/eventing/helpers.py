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
A collection of helper functions for streaming events.
"""


import os
import json
import time

from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()

GCP_PROJECT_ID = os.environ.get('GCP_PROJECT_ID')

def stream_event(topic_name, event_type, event_context):
    """
    Helper function for publishing an event.

    Parameters:
       topic_name (str): The name of the Cloud Pub/Sub topic.
       event_type (str): The type of the event.
       event_context: The context of the event.

    Output:
       None.
    """
    topic_path = publisher.topic_path(GCP_PROJECT_ID, topic_name)
    request = {
        'event_type': event_type,
        'created_time': str(int(time.time())),
        'event_context': event_context
    }
    data = json.dumps(request).encode("utf-8")
    try:
        future = publisher.publish(topic_path, data)
        message_id = future.result()
        print(f"Published message {message_id} to {topic_path}")
    except Exception as e:
        print(f"Error publishing message: {e}")
