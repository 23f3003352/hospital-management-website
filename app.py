from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,BooleanField, TextAreaField, DateField, SubmitField, TimeField
from wtforms.validators import DataRequired, Email, equal_to
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from forms import RegistrationForm, LoginForm, DoctorForm, AppointmentForm, TimeSlotForm
from models import patient, doctor, appointment, timeSlot

secret_key = 'aksaslknmckjdnoaekmdaksmc'  # Replace with a secure key in production
app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # This give our code information of what, where and how our database is stored
db = SQLAlchemy(app) #creating an instance of SQLAlchemy so we can use it to interact with our database... like storing it in a variable and calling variable when we need to access it

# Creating Routes
@app.route('/')
def home():
    return "Welcome to the Home Page!"



if __name__ == "__main__":
    app.run(debug=True)