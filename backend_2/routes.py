from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import api, db
from models import User, Doctor
from auth import Register, Login


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

    def post(self):
        return {'post': 'hello world!'}


class DoctorResource(Resource):
    @jwt_required()
    def post(self):
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        if not user or user.role != 'admin':
            return {'msg': 'unauthorized'}, 401

        data = __import__('flask').flask.request.get_json() if False else None
        # use flask.request normally but avoid top-level import confusion in some linters; import here:
        from flask import request
        data = request.get_json() or {}

        doctor = Doctor(name=data.get('name'), specialization=data.get('specialization'), available=data.get('available', True))
        db.session.add(doctor)
        db.session.commit()
        return {'msg': 'doctor added'}, 201

    @jwt_required()
    def put(self, doctor_id):
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        if not user or user.role != 'admin':
            return {'msg': 'unauthorized'}, 401

        from flask import request
        data = request.get_json() or {}
        doctor = Doctor.query.get_or_404(doctor_id)
        doctor.name = data.get('name', doctor.name)
        doctor.specialization = data.get('specialization', doctor.specialization)
        doctor.available = data.get('available', doctor.available)
        db.session.commit()
        return {'msg': 'doctor updated'}

    @jwt_required()
    def delete(self, doctor_id):
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        if not user or user.role != 'admin':
            return {'msg': 'unauthorized'}, 401

        doctor = Doctor.query.get_or_404(doctor_id)
        db.session.delete(doctor)
        db.session.commit()
        return {'msg': 'doctor deleted'}


# register resources on the Api instance
api.add_resource(HelloWorld, '/')
api.add_resource(DoctorResource, '/doctor', '/doctor/<int:doctor_id>')
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
