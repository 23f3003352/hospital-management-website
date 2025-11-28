# run.py

from app import app
# You MUST import all your models here
# This is what registers them with SQLAlchemy
from models import patient, doctor, appointment, timeSlot
from flask_migrate import Migrate
from extension import migrate
from extension import db

# Create an application context
from app import app, db
from models import patient
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    print("All tables created.")

    admin = patient(
        username="admin",
        name="Admin",
        age=30,
        password=generate_password_hash("admin123"),
        is_admin=True,
        is_doctor=False
    )
    db.session.add(admin)
    db.session.commit()
    print("Admin created!")

    admin = doctor(
        username="admin",
        name="Admin",
        specialization="admin",
        password=generate_password_hash("admin123"),
        is_admin=True,
        is_doctor=False
    )
    db.session.add(admin)
    db.session.commit()
    print("Admin created!")

# from app import app, db

# with app.app_context():
#     db.create_all()
#     print("All tables created.")
