from flask_login import UserMixin
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from extension import db

class patient(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    appointments = db.relationship('appointment', back_populates='patient', lazy=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_doctor = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Patient('{self.name}', '{self.username}')"
    
class doctor(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    availability = db.Column(db.Date, nullable=True)
    timeSlots = db.relationship('timeSlot', back_populates='doctor', lazy=True)
    appointments = db.relationship('appointment', back_populates='doctor', lazy=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_doctor = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"Doctor('{self.name}', '{self.specialization}')"
    
class appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    slot = db.Column(db.String(20), nullable=False)
    prescription = db.Column(db.Text, nullable=True)
    status = db.Column(db.Boolean, default=False)

    # this allows us to access related patient and doctor easily
    doctor = db.relationship('doctor', back_populates='appointments', lazy=True)
    patient = db.relationship('patient', back_populates='appointments', lazy=True)

    def __repr__(self):
        return f"Appointment(Patient ID: '{self.patient_id}', Doctor ID: '{self.doctor_id}', Date: '{self.appointment_date}', Time: '{self.appointment_time}')"
    
class timeSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_time = db.Column(db.Time, nullable=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    
    doctor = db.relationship('doctor', back_populates='timeSlots', lazy=True)

    def __repr__(self):
        return f"TimeSlot('{self.appointment_time}')"