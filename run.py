# made to create all database tables
# init_db.py

from app import app, db

# Import all your models here so SQLAlchemy knows about them
from models import patient, doctor, appointment, timeSlot

def create_tables():
    print("Creating database tables...")
    with app.app_context():
        db.create_all()
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_tables()