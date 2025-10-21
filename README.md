# hospital-management-website
This is a website made using HTML, CSS, Python, Bootstrap, Flask and Jinja2. 

Hospital Management System (HMS)
This project is a web application for a Hospital Management System (HMS) built for the Modern Application Development I course. It provides a centralized platform for Admins, Doctors, and Patients to manage hospital operations efficiently.


Problem Statement
Many hospitals currently rely on manual registers or disconnected software systems. This makes it difficult to manage patient records, track patient history effectively, avoid scheduling conflicts, and streamline overall operations. This project aims to solve these issues by creating a single, integrated web application.

Core Features
The system is built with three distinct user roles: Admin, Doctor, and Patient.

1. Admin (Hospital Staff)
The Admin is a pre-existing superuser; no registration is allowed for this role.



Dashboard: View system statistics, including the total number of doctors, patients, and appointments.


Doctor Management: Add, update, and delete doctor profiles, including their name, specialization, and availability.



Patient Management: Can search for patients by name, ID, or contact information.



Appointment Management: View and manage all appointments in the system (both upcoming and past).



User Management: Can remove or "blacklist" doctors and patients from the system.

2. Doctor

Dashboard: View assigned appointments for the day or week and see a list of assigned patients.




Availability: Can provide and update their availability for the next 7 days.


Appointment Workflow: Mark appointments as "Completed" or "Cancelled".




Treatment Records: Enter diagnosis, treatment notes, and prescriptions after a visit is completed.



Patient History: View the complete medical history (previous diagnoses, prescriptions) for their patients.


3. Patient

Authentication: Can register for a new account, log in, and update their personal profile.




Doctor Search: Search for doctors by specialization or name and view their profiles and availability for the next 7 days.




Appointment Booking: Can book, reschedule, or cancel their own appointments based on doctor availability.



Dashboard: View all available specializations/departments.


Medical History: View their own upcoming appointments and status as well as their past appointment history with diagnosis and prescription details.




Key System Functionalities

Conflict Prevention: Prevents multiple appointments from being booked for the same doctor at the same date and time.


Dynamic Status: Appointment statuses are updated dynamically (e.g., Booked, Completed, Cancelled).


History Tracking: Stores all completed appointment records, including diagnosis, prescriptions, and notes, for every patient.

Technology Stack
This project is built using the following mandatory frameworks and technologies:


Backend: Flask 


Frontend: Jinja2 Templating, HTML, CSS 



Styling: Bootstrap 



Database: SQLite 


Authentication (Recommended): Flask-Login / Flask-Security