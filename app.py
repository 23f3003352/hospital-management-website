from flask import Flask, render_template, flash, redirect, session, url_for, request
from flask_wtf import CSRFProtect, FlaskForm
from wtforms import StringField, PasswordField,BooleanField, TextAreaField, DateField, SubmitField, TimeField
from wtforms.validators import DataRequired, Email, equal_to
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime, timedelta
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from extension import db, login_manager


secret_key = 'aksaslknmckjdnoaekmdaksmc'  # Replace with a secure key in production
app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # This give our code information of what, where and how our database is stored
#db = SQLAlchemy(app) #creating an instance of SQLAlchemy so we can use it to interact with our database... like storing it in a variable and calling variable when we need to access it
db.init_app(app)

from forms import RegistrationForm, LoginForm, DoctorForm, AppointmentForm, TimeSlotForm
from models import patient, doctor, appointment, timeSlot

# login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'  # specify the login view for @login_required

@login_manager.user_loader
def load_user(user_id):
    user_type = session.get("user_type")

    if user_type == "doctor":
        return doctor.query.get(int(user_id))

    # Default to patient (patient + admin are both here)
    return patient.query.get(int(user_id))

@app.context_processor
def inject_user():
    return dict(current_user=current_user, request = request)


# Creating Routes

@app.route('/debug')
@login_required
def debug():
    return f"""
    <h3>User Debug</h3>
    ID: {current_user.id}<br>
    Is Admin: {current_user.is_admin}<br>
    Is Doctor: {current_user.is_doctor}<br>
    Username: {current_user.username}<br>
    Type: {type(current_user)}<br>
    """

@app.route('/routes')
def routes():
    import urllib
    output = "<h2>All Routes</h2><ul>"
    for rule in app.url_map.iter_rules():
        output += f"<li>{rule.endpoint} → {rule.rule}</li>"
    output += "</ul>"
    return output



@app.route("/")
def default():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    today = date.today()
    next_week = today + timedelta(days=7)

    # Common filter for all
    base_filter = (
        appointment.appointment_date >= today,
        appointment.appointment_date <= next_week
    )

    if current_user.is_admin:
        appts = appointment.query.filter(
            *base_filter,
            appointment.is_blocked == False,
            appointment.patient_id != 0
        ).order_by(
            appointment.appointment_date.asc()
        ).all()
        return render_template('home_da.html', appointments=appts)

    elif current_user.is_doctor:
        appts = appointment.query.filter(
            appointment.doctor_id == current_user.id,
            *base_filter,
            appointment.is_blocked == False,
            appointment.patient_id != 0
        ).order_by(
            appointment.appointment_date.asc()
        ).all()
        return render_template('home_d.html', appointments=appts)

    else:
        appts = appointment.query.filter(
            appointment.patient_id == current_user.id,
            *base_filter,
            appointment.is_blocked == False,
            appointment.patient_id != 0
        ).order_by(
            appointment.appointment_date.asc()
        ).all()
        return render_template('home_p.html', appointments=appts)

            
@app.route('/doctor_list', methods=['GET', 'POST'])
def Doctor():
        q = request.args.get("q", "")  # get search text, default empty

        if q:
            doctors = doctor.query.filter(
                (doctor.name.ilike(f"%{q}%")) |
                (doctor.specialization.ilike(f"%{q}%"))
            ).all()
        else:
            doctors = doctor.query.all()

        return render_template('doctor.html', doctors=doctors, q=q)

@app.route('/patient', methods=['GET', 'POST'])
def Patient():

    q = request.args.get("q", "")  # get search text, default empty
    if q:
        pat = patient.query.filter(
            (patient.name.ilike(f"%{q}%")) |
            (patient.username.ilike(f"%{q}%"))
        ).all()
    else:
        pat = patient.query.all()
    return render_template('patient.html', patient=pat)

@app.route('/appointment', methods=['GET', 'POST'])
def Appointment():
    if current_user.is_admin:
            appts = appointment.query.filter(
            appointment.is_blocked == False,
            appointment.patient_id != 0
        ).order_by(
            appointment.appointment_date.asc()
        ).all()
    elif current_user.is_doctor:
        appts = appointment.query.filter(
            appointment.doctor_id == current_user.id,
            appointment.is_blocked == False,
            appointment.patient_id != 0
        ).order_by(
            appointment.appointment_date.asc()
        ).all()
    else:
        appts = appointment.query.filter(
            appointment.patient_id == current_user.id,
            appointment.is_blocked == False,
            appointment.patient_id != 0
        ).order_by(
            appointment.appointment_date.asc()
        ).all()
    return render_template('appointment_history.html', appointments=appts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = patient.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('That username is already taken. Please choose a different one.', 'danger')
            return render_template('register.html', form=form)
        if form.validate_on_submit():
            hashed_password = generate_password_hash(form.password.data)
            new_user = patient(username=form.username.data, name=form.name.data, age=form.age.data, password=hashed_password, is_admin=False, is_doctor=False)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash('Your account has been created!', 'success')
            return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = patient.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                session["user_type"] = "patient"
                flash(f'Welcome back {user.username}!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check your password.', 'danger')
        else:
            flash('Login Unsuccessful. User does not exist.', 'danger')
    return render_template('login.html', form=form)

@app.route('/login_doctor', methods=['GET', 'POST'])
def login_doctor():
    form = LoginForm()
    if form.validate_on_submit():
        if user := doctor.query.filter_by(username=form.username.data).first():
            if user and check_password_hash(user.password, form.password.data):
                login_user(user)
                session["user_type"] = "doctor"
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login_d.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop("user_type", None)
    flash("Logged out successfully!", "success")
    return redirect(url_for('login'))


@app.route('/addDoctor', methods=['GET', 'POST'])
@login_required
def addDoctor():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))
    form = DoctorForm()
    if form.validate_on_submit():
        existing_user = doctor.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('That username is already taken. Please choose a different one.', 'danger')
            return render_template('register_d.html', form=form)
        hashed_password = generate_password_hash(form.password.data)
        new_doc = doctor(
            username=form.username.data,
            name=form.name.data,
            specialization=form.specialization.data,
            password=hashed_password,
            is_doctor=True,
            is_admin=False
        )
        db.session.add(new_doc)
        db.session.commit()
        flash('Doctor added successfully!', 'success')
        return redirect(url_for('Doctor'))
    return render_template('register_d.html', form=form)

@app.route('/delete_doctor/<int:doctor_id>', methods=['POST'])
@login_required
def delete_doctor(doctor_id):
    # Only admin allowed
    if not current_user.is_admin:
        flash("You do not have permission to delete doctors.", "danger")
        return redirect(url_for('home'))

    doc = doctor.query.get_or_404(doctor_id)

    # Delete all appointments first (or else FK constraint issues)
    for a in doc.appointments:
        db.session.delete(a)

    # Delete timeslots linked to doctor
    for t in doc.timeSlots:
        db.session.delete(t)

    # Finally delete doctor
    db.session.delete(doc)
    db.session.commit()

    flash("Doctor deleted successfully.", "success")
    return redirect(url_for('Doctor'))

@app.route('/doctor/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
def doctor_profile(doctor_id):
    doc = doctor.query.get_or_404(doctor_id)
    form = AppointmentForm()

    # Generate the next 7 days
    today = date.today()
    days = [today + timedelta(days=i) for i in range(7)]

    # Slot labels (slot_1, slot_2, slot_3)
    slot_map = {
        "9 AM - 12 PM": "9 AM - 12 PM",
        "12 PM - 3 PM": "12 PM - 3 PM",
        "3 PM - 6 PM": "3 PM - 6 PM"
    }

    # Availability dictionary
    availability = {}
    for day in days:
        availability[day] = {}
        for slot_key in slot_map.keys():
            booked = appointment.query.filter(
                appointment.doctor_id == doctor_id,
                appointment.appointment_date == day,
                appointment.slot == slot_key,
                appointment.is_blocked == False,
                appointment.patient_id != 0
            ).first()
            availability[day][slot_key] = (booked is None)

    if form.validate_on_submit():

        selected_date = form.appointment_date.data
        selected_slot = form.slot.data

        # If doctor → slot becomes unavailable
        if current_user.is_doctor and current_user.id == doctor_id:
            new_block = appointment(
                patient_id=0,  # unused but required
                doctor_id=doctor_id,
                appointment_date=selected_date,
                slot=selected_slot,
                is_blocked=True
            )
            db.session.add(new_block)
            db.session.commit()
            flash("Slot marked unavailable!", "success")
            return redirect(url_for('doctor_profile', doctor_id=doctor_id))

        # If patient → normal appointment
        new_appt = appointment(
            patient_id=current_user.id,
            doctor_id=doctor_id,
            appointment_date=selected_date,
            slot=selected_slot,
            is_blocked=False
        )
        db.session.add(new_appt)
        db.session.commit()
        flash("Appointment booked!", "success")
        return redirect(url_for('doctor_profile', doctor_id=doctor_id))

    
    return render_template(
        'profile_page_d.html',
        doc=doc,
        form=form,
        days=days,
        slot_map=slot_map,
        availability=availability
    )

@app.route('/patient/<int:patient_id>')
@login_required
def patient_profile(patient_id):
    pat = patient.query.get_or_404(patient_id)

    appointments = appointment.query.filter(
        appointment.patient_id == patient_id,
        appointment.is_blocked == False,
        appointment.patient_id != 0
    ).order_by(
        appointment.appointment_date.asc()
    ).all()

    return render_template(
        'profile_page_p.html',
        pat=pat,
        appointments=appointments
    )


@app.route('/profile')
@login_required
def profile():
    if current_user.is_doctor:
        return redirect(url_for('doctor_profile', doctor_id=current_user.id))
    if current_user.is_admin:
        return redirect(url_for('doctor_profile', doctor_id=current_user.id))
    else:
        return redirect(url_for('patient_profile', patient_id=current_user.id))

@app.route('/mark_done/<int:appt_id>', methods=['POST'])
@login_required
def mark_done(appt_id):
    a = appointment.query.get_or_404(appt_id)

    # Allow: doctor who owns this appointment OR admin
    if not (current_user.is_admin or 
            (current_user.is_doctor and a.doctor_id == current_user.id)):
        flash("Not allowed.", "danger")
        return redirect(url_for('Appointment'))

    # Toggle status
    a.status = not a.status
    db.session.commit()

    flash("Status updated!", "success")
    return redirect(url_for('Appointment'))


@app.route('/add_notes/<int:appt_id>', methods=['POST', 'GET'])
@login_required
def add_notes(appt_id):
    a = appointment.query.get_or_404(appt_id)

    if not (current_user.is_admin or 
            (current_user.is_doctor and a.doctor_id == current_user.id)):
        flash("Not allowed.", "danger")
        return redirect(url_for('Appointment'))

    if request.method == "POST":
        new_notes = request.form.get("prescription")  # <-- FIXED LINE
        print("Received prescription:", new_notes)

        a.prescription = new_notes
        db.session.commit()

        flash("Prescription updated!", "success")
        return redirect(url_for('Appointment'))

    return render_template("add_notes.html", appt=a)

@app.route('/view_notes/<int:appt_id>')
@login_required
def view_notes(appt_id):
    a = appointment.query.get_or_404(appt_id)

    # Anyone involved (doctor, patient, admin) can view
    return render_template("add_notes.html", appt=a, view_only=True)

@app.route('/cancel_appointment/<int:appt_id>', methods=['POST'])
@login_required
def cancel_appointment(appt_id):
    a = appointment.query.get_or_404(appt_id)

    # Only the patient who booked it can cancel
    if a.patient_id != current_user.id:
        flash("You can't cancel someone else's appointment!", "danger")
        return redirect(url_for('Appointment'))

    db.session.delete(a)
    db.session.commit()
    flash("Appointment cancelled.", "success")
    return redirect(url_for('Appointment'))

@app.route('/unblock_slot/<int:appt_id>', methods=['POST'])
@login_required
def unblock_slot(appt_id):
    a = appointment.query.get_or_404(appt_id)

    # Only the doctor who owns this slot can unblock
    if not (current_user.is_doctor and a.doctor_id == current_user.id and a.is_blocked):
        flash("You cannot unblock this slot.", "danger")
        return redirect(url_for('doctor_profile', doctor_id=current_user.id))

    db.session.delete(a)
    db.session.commit()
    flash("Slot unblocked.", "success")

    return redirect(url_for('doctor_profile', doctor_id=current_user.id))


@app.route('/reschedule/<int:appt_id>', methods=['GET', 'POST'])
@login_required
def reschedule(appt_id):
    a = appointment.query.get_or_404(appt_id)

    # Only the patient who booked OR admin can reschedule
    if current_user.id != a.patient_id and not current_user.is_admin:
        flash("You are not allowed to reschedule this appointment.", "danger")
        return redirect(url_for('Appointment'))

    doctor_id = a.doctor_id
    today = date.today()
    days = [today + timedelta(days=i) for i in range(7)]
    days.sort()

    slot_map = [
        "9 AM - 12 PM",
        "12 PM - 3 PM",
        "3 PM - 6 PM"
    ]

    selected_date = request.args.get("date")
    available_slots = []

    # Step 1 → user selected a date → show available slots
    if selected_date:
        selected_date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date()

        for slot in slot_map:
            booked = appointment.query.filter(
                appointment.doctor_id == doctor_id,
                appointment.appointment_date == selected_date_obj,
                appointment.slot == slot,
                appointment.is_blocked == False,
                appointment.patient_id != 0
            ).first()

            # Slot is free if:
            # - No booking found
            # - Or the booking is THIS SAME APPOINTMENT (editing case)
            if booked is None or booked.id == appt_id:
                available_slots.append(slot)

    # Step 2 → final confirmation POST
    if request.method == "POST":
        new_date = request.form.get("new_date")
        new_slot = request.form.get("new_slot")

        new_date_obj = datetime.strptime(new_date, "%Y-%m-%d").date()

        # Backend safety — prevent overlap
        conflict = appointment.query.filter(
            appointment.doctor_id == doctor_id,
            appointment.appointment_date == new_date_obj,
            appointment.slot == new_slot,
            appointment.id != appt_id,
            appointment.is_blocked == False,
            appointment.patient_id != 0
        ).first()

        if conflict:
            flash("That slot is already booked!", "danger")
            return redirect(url_for('reschedule', appt_id=appt_id))

        # Apply the update
        a.appointment_date = new_date_obj
        a.slot = new_slot
        db.session.commit()

        flash("Appointment rescheduled!", "success")
        return redirect(url_for('Appointment'))

    # Render page
    return render_template(
        "reschedule.html",
        appt=a,
        days=days,
        selected_date=selected_date,
        slots=available_slots
    )



if __name__ == "__main__":
    app.run(debug=True)