from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, SelectField, StringField, PasswordField, SubmitField, BooleanField, TextAreaField, TimeField
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
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    specialization = StringField('Specialization', validators=[DataRequired()])
    availability = DateField('Availability')
    submit = SubmitField('Add Doctor')

class AppointmentForm(FlaskForm):
    appointment_date = DateField('Appointment Date', validators=[DataRequired()])
    slot = StringField('Slot', validators=[DataRequired()])
    submit = SubmitField('Book Appointment')

class TimeSlotForm(FlaskForm):
    appointment_time = TimeField('Appointment Time', validators=[DataRequired()])
    submit = SubmitField('Add Time Slot')
