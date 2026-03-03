from flask import Blueprint, request, jsonify
from .models import File
from . import db
from .storage_mode import upload_file, delete_file

bp = Blueprint('api', __name__, url_prefix = '/api')

@bp.get("/health")
def health():
    return jsonify({"status" : "ok"}), 200

@bp.post("/upload")
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
def list_files():
    pass

@bp.delete("/delete/{id}")
def delete():
    pass