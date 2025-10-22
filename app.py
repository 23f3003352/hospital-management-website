from flask import Flask, render_template

app = Flask(__name__)

# Creating Routes
@app.route('/')
def home():
    return "Welcome to the Home Page!"