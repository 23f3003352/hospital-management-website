from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, StringField, PasswordField, SubmitField, BooleanField, TextAreaField, TimeField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class DoctorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    specialization = StringField('Specialization', validators=[DataRequired()])
    availability = DateField('Availability')
    submit = SubmitField('Add Doctor')

class AppointmentForm(FlaskForm):
    patient_id = StringField('Patient ID', validators=[DataRequired()])
    doctor_id = StringField('Doctor ID', validators=[DataRequired()])
    appointment_date = DateField('Appointment Date', validators=[DataRequired()])
    appointment_time = TimeField('Appointment Time', validators=[DataRequired()])
    prescription = TextAreaField('Prescription')
    status = BooleanField('Status')
    submit = SubmitField('Book Appointment')

class TimeSlotForm(FlaskForm):
    appointment_time = TimeField('Appointment Time', validators=[DataRequired()])
    submit = SubmitField('Add Time Slot')
