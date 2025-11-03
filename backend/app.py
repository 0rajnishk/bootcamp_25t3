import json
from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required,  get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["JWT_SECRET_KEY"] = "super-secret" 

api = Api(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)




# Models 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number =db.Column(db.String(10), unique=True,nullable=False)
    password =db.Column(db.String(200),nullable=False)
    role = db.Column(db.String(20), nullable=False, default='patient') # admin, doctor, patient
    
    def to_json(self):
        return {
            "username":self.username,
            "email":self.email,
            "phone_number":self.phone_number,
            "role": self.role
        }

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    specialization = db.Column(db.String(120), nullable=False)
    available = db.Column(db.Boolean, default=True)


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date_time = db.Column(db.String(100))
    status = db.Column(db.String(100)) # complete, cancel
    notes = db.Column(db.String(200))


with app.app_context():
    db.create_all()





class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}
    
    def post(self):
        return {'post': 'hello world!'}


class Register(Resource):
    @jwt_required()
    def get(self):
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        if user.role != 'admin':
            return {'msg':'unauthorized'}, 401

        # user = User.query.filter_by(username=username).first()
        # users = User.query.all()
        # user_json = []
        # for user in users:
        #     user_json.append(user.to_json())

        # user_id = 1
        # user = User.query.get(user_id)

        return {'user':user, 'msg':'', 'error':''}, 200

    def post(self):
        data = request.get_json()
        password_hash = generate_password_hash(data['password'])
        try:
            user = User(username=data['username'], email=data['email'], phone_number=data['phone_number'], password=password_hash)
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            print('error')
            return('error')
        return {'msg':'success'}


class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if not user:
            return {'msg': 'no such username'}

        if check_password_hash(data['password'], user.password):
            return {'msg': 'incorrect password'}
        
        token = create_access_token(identity=user.username)
        return {'msg':'login successful', 'token':token}


class DoctorResource(Resource):
    @jwt_required()
    def post(self):
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        if user.role != 'admin':
            return {'msg':'unauthorized'}, 401
        
        data = request.get_json()
        doctor = Doctor(name=data['name'], specialization=data['specialization'], available=data.get('available', True))
        db.session.add(doctor)
        db.session.commit()
        return {'msg': 'doctor added'}, 201
    

    @jwt_required()
    def put(self, doctor_id):
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        if user.role != 'admin':
            return {'msg':'unauthorized'}, 401
        
        data = request.get_json()
        doctor = Doctor.query.get_or_404(doctor_id)
        doctor.name = data['name']
        doctor.specialization = data['specialization']
        doctor.available = data['available']
        db.session.commit()
        return {'msg': 'doctor updated'}
    
    @jwt_required()
    def delete(self, doctor_id):
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        if user.role != 'admin':
            return {'msg':'unauthorized'}, 401

        doctor = Doctor.query.get_or_404(doctor_id)
        db.session.delete(doctor)
        db.session.commit()
        return {'msg':'doctor deleted'}
api.add_resource(DoctorResource, '/doctor', '/doctor/<int:doctor_id>')


api.add_resource(HelloWorld, '/')
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')



if __name__ == '__main__':
    app.run(debug=True)
