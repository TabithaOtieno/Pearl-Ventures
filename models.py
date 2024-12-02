from init_db import db

# db model
class EmployeeDetails(db.Model):
    __tablename__ = 'employee_details'
    employee_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False, unique=True)
    id_number = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    kra_pin = db.Column(db.String(20), nullable=False, unique=True)
    employee_position = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    id = db.Column(db.Integer, primary_key=True)

