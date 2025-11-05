from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from models import User
from extensions import db


class Register(Resource):
    """POST /register to create a new user (open).
    GET /register returns all users and requires an admin JWT.
    """

    @jwt_required()
    def get(self):
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        if not user or user.role != 'admin':
            return {'msg': 'unauthorized'}, 401
        users = [u.to_json() for u in User.query.all()]
        return {'users': users}, 200

    def post(self):
        data = request.get_json() or {}
        required = ('username', 'email', 'phone_number', 'password')
        for r in required:
            if r not in data:
                return {'msg': f'missing {r}'}, 400

        if User.query.filter_by(username=data['username']).first():
            return {'msg': 'username already exists'}, 400

        password_hash = generate_password_hash(data['password'])
        try:
            user = User(username=data['username'], email=data['email'], phone_number=data['phone_number'], password=password_hash)
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'msg': 'error', 'error': str(e)}, 500
        return {'msg': 'success'}, 201


class Login(Resource):
    def post(self):
        data = request.get_json() or {}
        if 'username' not in data or 'password' not in data:
            return {'msg': 'username and password required'}, 400

        user = User.query.filter_by(username=data['username']).first()
        if not user:
            return {'msg': 'no such username'}, 404

        # check_password_hash(stored, candidate_password)
        if not check_password_hash(user.password, data['password']):
            return {'msg': 'incorrect password'}, 401

        token = create_access_token(identity=user.username)
        return {'msg': 'login successful', 'token': token}, 200
