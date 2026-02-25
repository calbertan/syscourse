# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_admin import initialize_app, firestore
from firebase_functions import https_fn
import flask
from flask import jsonify

from dataclasses import asdict, dataclass, field
from typing import Optional

# Assuming the Resource dataclass is defined here for simplicity
@dataclass
class Resource:
    course_id: str
    title: str
    type: str
    url: str
    description: str
    uid: str
    thumbnail: str
    duration: Optional[int] = None
    document_id: Optional[str] = None
    resource_id: Optional[str] = None

    @staticmethod
    def deserialize(document):
        data = document.to_dict()
        return Resource(
            course_id=data.get("course_id"),
            title=data.get("title"),
            type=data.get("type"),
            url=data.get("url"),
            description=data.get("description"),
            uid=data.get("uid"),
            thumbnail=data.get("thumbnail"),
            duration=data.get("duration"),
            document_id=document.id,
            resource_id=document.id,
        )

initialize_app()
app = flask.Flask(__name__)

# Build multiple CRUD interfaces:


@app.get("/resources")
@app.get("/resources/<resource_id>")
def get_resource(resource_id=None):
    if resource_id is not None:
        # Retrieve a single document by its ID
        document_snapshot = firestore.client().collection("resources").document(resource_id).get()
        if document_snapshot.exists:
            document_data = document_snapshot.to_dict()
            document_data['resource_id'] = document_snapshot.id  # Add the document ID to the response
            return document_data
        else:
            return {"error": "Document not found"}, 404
    else:
        # Retrieve all documents in the collection, ordered by title
        documents = firestore.client().collection("resources").order_by("title").get()
        documents_list = []
        for document in documents:
            document_data = document.to_dict()
            document_data['resource_id'] = document.id  # Add the document ID to each document's data
            documents_list.append(document_data)
        return documents_list

@app.get("/resources/course/<course_id>")
def list_resources_by_course_endpoint(course_id):
    query = firestore.client().collection("resources").where("course_id", "==", course_id).get()
    resources = [Resource.deserialize(doc) for doc in query if doc.exists]
    return jsonify([asdict(resource) for resource in resources]), 200

@app.post("/resources")
def add_resource():
    data = flask.request.get_json()
    if not data:
         return jsonify({"error": "No data provided"}), 400
    
    doc_ref = firestore.client().collection("resources").document()
    write_result = doc_ref.set(data)  # This line actually writes the data to Firestore
    return jsonify({"success": True, "doc_id": doc_ref.id}), 201

@app.delete("/resources/<resource_id>")
def delete_resource_endpoint(resource_id):
    firestore.client().collection("resources").document(resource_id).delete()
    return jsonify({"message": "Resource deleted"}), 200


# Expose Flask app as a single Cloud Function:


@https_fn.on_request()
def flask_app(req: https_fn.Request) -> https_fn.Response:
    with app.request_context(req.environ):
        return app.full_dispatch_request()
