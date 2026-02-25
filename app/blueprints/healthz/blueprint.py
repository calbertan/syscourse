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
This module is the Flask blueprint for the product catalog page (/).
"""


from flask import Blueprint, jsonify


healthz_page = Blueprint('healthz_page', __name__)


@healthz_page.route('/healthz')
def health_check():
    """
    Health check endpoint.
    Returns a simple HTTP 200 response to indicate the application is running.
    """
    return jsonify({"status": "ok"}), 200