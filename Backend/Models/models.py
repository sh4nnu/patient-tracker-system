from app import db
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure secret key

db = SQLAlchemy(app)
admin = Admin(app, name='Patient Tracker Admin', template_mode='bootstrap3')


class User(db.Model):
    '''
    User model for the database.
    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    #password = db.Column(db.String(80), nullable=False)
    #email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    # is_admin = db.Column(db.Boolean, default=False)
    # is_active = db.Column(db.Boolean, default=True)
    # is_superuser = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime, nullable=True)
    date_joined = db.Column(db.DateTime, nullable=False)

class Patient(db.Model):
    '''
    Patient model for the database.
    '''
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    gender = db.Column(db.String(10), nullable=True)
    contact_number = db.Column(db.String(15), nullable=True)
    address = db.Column(db.String(200), nullable=True)

class Doctor(db.Model):
    '''
    Doctor model for the database.
    '''
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    credentials = db.Column(db.String(100), nullable=False)

class Medicine(db.Model):
    '''
    Medicine model for the database.
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    medication_id = db.Column(db.Integer, nullable=False)
    dosage = db.Column(db.String(50), nullable=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    prescription_date = db.Column(db.Date, nullable=False)
    medical_record_id = db.Column(db.Integer, db.ForeignKey('medical_record.id'), nullable=False)


class MedicalRecord(db.Model):
    '''
    MedicalRecord model for the database.
    '''
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    diagnosis = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)
    record_id = db.Column(db.Integer, nullable=False)
    medication_id = db.Column(db.Integer, db.ForeignKey('medicine.id'), nullable=True)

# Add models to the admin interface
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Patient, db.session))
admin.add_view(ModelView(Doctor, db.session))
admin.add_view(ModelView(Medicine, db.session))
admin.add_view(ModelView(MedicalRecord, db.session))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)