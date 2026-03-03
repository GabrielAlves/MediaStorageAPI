from flask import Blueprint, request, jsonify
from .models import File
from . import db
from .auth import require_api_key
from .storage_mode import upload_file, delete_file
import uuid
import os

bp = Blueprint('api', __name__)

@bp.get("/health")
@require_api_key
def health():
    return jsonify({"status" : "ok"}), 200

@bp.post("/upload")
@require_api_key
def upload():
    if "file" not in request.files:
        return jsonify({"error" : "no file provided"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    file_type = file.mimetype.split("/")[0]

    url = upload_file(file)

    db_file = File(file_name = file.filename,
                      file_type = file_type,
                      file_url = url
                    )

    db.session.add(db_file)
    db.session.commit()

    return jsonify({"message" : "File uploaded", "id" : db_file.id}), 201

@bp.get("/list")
@require_api_key
def list_files():
    db_files = File.query.all()

    results = [
        {
            "id" : f.id,
            "file_name" : f.file_name,
            "file_type" : f.file_type,
            "file_url" : f.file_url,
            "created_at" : f.created_at
        } for f in db_files
    ]

    return jsonify(results), 200

@bp.delete("/delete/<int:id>")
@require_api_key
def delete(id):
    db_file = File.query.get_or_404(id)

    delete_file(db_file.file_name)

    db.session.delete(db_file)
    db.session.commit()

    return jsonify({"message" : "File deleted"}), 200