from datetime import datetime
from . import db

# TODO: decrease size to the minimum after tests are done
class File(db.Model):
    id = db.Column(db.Integer, primary_key = True, index = True)
    file_name = db.Column(db.String(255), nullable = False)
    file_type = db.Column(db.String(30), nullable = False)
    file_url = db.Column(db.String(500), nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)