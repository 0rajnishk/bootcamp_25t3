from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restful import Api


# Initialize extensions without app to avoid circular imports.
# They'll be initialized inside create_app() via .init_app(app).

db = SQLAlchemy()
jwt = JWTManager()
api = Api()
