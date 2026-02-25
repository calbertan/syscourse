# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_admin import initialize_app, firestore
from firebase_functions import https_fn
import flask
from flask import jsonify

from dataclasses import asdict, dataclass, field
from typing import Optional


@dataclass
class Course:
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
        data = document.to_dict()
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


initialize_app()
app = flask.Flask(__name__)

# Build multiple CRUD interfaces:


@app.get("/courses")
@app.get("/courses/<course_id>")
def get_course(course_id=None):
    if course_id is not None:
        # Retrieve a single document by its ID
        document_snapshot = (
            firestore.client().collection("courses").document(course_id).get()
        )
        if document_snapshot.exists:
            document_data = document_snapshot.to_dict()
            document_data["course_id"] = (
                document_snapshot.id
            )  # Add the document ID to the response
            return document_data
        else:
            return {"error": "Document not found"}, 404
    else:
        # Retrieve all documents in the collection, ordered by title
        documents = firestore.client().collection("courses").order_by("title").get()
        documents_list = []
        for document in documents:
            document_data = document.to_dict()
            document_data["course_id"] = (
                document.id
            )  # Add the document ID to each document's data
            documents_list.append(document_data)
        return documents_list


@app.post("/courses")
def add_resource():
    data = flask.request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    doc_ref = firestore.client().collection("courses").document()
    write_result = doc_ref.set(data)  # This line actually writes the data to Firestore
    return jsonify({"success": True, "doc_id": doc_ref.id}), 201


@app.delete("/courses/<course_id>/<uid>")
def delete_resource_endpoint(course_id, uid):
    course_ref = firestore.client.collection('courses').document(course_id)
    course_doc = course_ref.get()
    if course_doc.exists:
        course_data = course_doc.to_dict()
        if course_data['uid'] == uid:
            # Delete the course
            course_ref.delete()
            return jsonify({"message": "Resource deleted"}), 200
        else:
            return jsonify({"message": "Unauthorized"}), 401
    else:
        return jsonify({"message": "Cannot find course"}), 404


# Expose Flask app as a single Cloud Function:


@https_fn.on_request()
def course_helper(req: https_fn.Request) -> https_fn.Response:
    with app.request_context(req.environ):
        return app.full_dispatch_request()
