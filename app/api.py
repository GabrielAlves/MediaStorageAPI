from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)

bp = Blueprint('api', __name__, url_prefix = '/api')

@bp.get("/health")
def health():
    return {"status" : "ok"}

@bp.post("/upload")
def upload_file():
    pass

@bp.get("/list")
def list_files():
    pass

@bp.delete("/delete/{id}")
def delete_file():
    pass