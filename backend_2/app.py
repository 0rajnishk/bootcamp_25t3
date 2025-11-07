from flask import Flask
from config import Config
from extensions import db, jwt, api
from flask_cors import CORS

# Import routes to register resources onto `api`
import routes  # noqa: F401 - modules register resources at import time


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    # initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    api.init_app(app)

    # create DB
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
