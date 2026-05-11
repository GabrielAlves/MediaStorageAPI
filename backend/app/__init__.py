from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app(test_config = None):
    app = Flask(__name__)
    CORS(
        app,
        origins=[
                    "http://localhost:5001"
                ]
    )

    if test_config:
        app.config.update(test_config)

    else:
        from .config import Config
        app.config.from_object(Config)

    from . import routes
    app.register_blueprint(routes.bp)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app