from app import app
from init_db import db
from flask import request, jsonify
from models import EmployeeDetails

# Register employees
@app.route('/registration', methods=['POST'])
def register():
            
    data = request.json

    # Get data 
    employee_name = data.get('employee_name')
    phone_number = data.get('phone_number')
    id_number = data.get('id_number')
    email = data.get('email')
    kra_pin = data.get('kra_pin')
    employee_position = data.get('employee_position')
    salary = data.get('salary')

    # Ensure all fields are required
    if not employee_name or not phone_number or not id_number or not email or not kra_pin or not employee_position or not salary:
        return jsonify({'success': False,'message': 'All fields are required.'}), 400
    
    # Check if the details are unique
    employee_exists = EmployeeDetails.query.filter(
        (EmployeeDetails.phone_number == phone_number) |
        (EmployeeDetails.id_number == id_number) |
        (EmployeeDetails.email == email) |
        (EmployeeDetails.kra_pin == kra_pin)
    ).first()

    if employee_exists:
        return jsonify({
            'success': False,
            'message': 'Employee details already exist.'
            }), 400

    # Save to database
    new_record = EmployeeDetails(
        employee_name=employee_name,
        phone_number=phone_number,
        id_number=id_number,
        email=email,
        kra_pin=kra_pin,
        employee_position=employee_position,
        salary=salary
    )

    try:
        db.session.add(new_record)
        db.session.commit()

        response = {
            'success': True,
            'message':"Employee registered successfully."
        }

        # Return a JSON response
        return jsonify(response)
    
    except Exception as e:
        # Handle errors
        db.session.rollback()
        return jsonify({
            'success': False, 
            'message': 'An error occurred while registering.',
            'error': str(e)
        }), 500
    
# Retrieve all employee details in a list
@app.route('/all_employees', methods=['GET'])
def get_all_employees():

    employees = EmployeeDetails.query.all()

    # If no employees are available
    if not employees:
        return jsonify({
            'success': False,
            'message': 'No employees found.'
            }), 200
    
    # Return all employee details as a JSON response
    return jsonify({
        'success': True,
        'data': [
            {
                'id': employee.id,
                'employee_name': employee.employee_name,
                'phone_number': employee.phone_number,
                'id_number': employee.id_number,
                'email': employee.email,
                'kra_pin': employee.kra_pin,
                'employee_position': employee.employee_position,
                'salary': employee.salary
            } for employee in employees
        ]
    })

# Retrieve particular employee details 
@app.route('/employee', methods=['GET'])
def get_employee():

    phone_number = request.args.get('phone_number')
    id_number = request.args.get('id_number')
    kra_pin = request.args.get('kra_pin')

    # Ensure at least one field is provided
    if not phone_number and not id_number and not kra_pin:
        return jsonify({'success': False,'message': 'At least one field is required.'}), 400
    
    # Fetch employee details based on unique identifier provided
    employee = EmployeeDetails.query.filter(
        (EmployeeDetails.phone_number == phone_number) |
        (EmployeeDetails.id_number == id_number) |
        (EmployeeDetails.kra_pin == kra_pin)
    ).first()

    # Where employee details are not found
    if not employee:
        return jsonify({
            'success': False,
            'message': 'Employee details not found.'
            }), 404
    
    # Return employee details as a JSON response
    return jsonify({
        'success': True,
        'data':{
            'employee_name': employee.employee_name,
            'phone_number': employee.phone_number,
            'id_number': employee.id_number,
            'email': employee.email,
            'kra_pin': employee.kra_pin,
            'employee_position': employee.employee_position,
            'salary': employee.salary
        }
        
    }), 200

# Update particular employee details
@app.route('/update_employee/<employee_id>', methods=['PUT'])
def update_employee(employee_id):
    
    data = request.json

    # Get employee details by id number
    employee = EmployeeDetails.query.get(employee_id)

    # If employee details are not found
    if not employee:
        return jsonify({
            'success': False,
            'message': 'ID Number does not exist.'
            }), 404
    
    # Update employee details
    employee.employee_name = data.get('employee_name', employee.employee_name)
    employee.phone_number = data.get('phone_number', employee.phone_number)
    employee.email = data.get('email', employee.email)
    employee.kra_pin = data.get('kra_pin', employee.kra_pin)
    employee.employee_position = data.get('employee_position', employee.employee_position)
    employee.salary = data.get('salary', employee.salary)

    # Save to database
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Employee details updated successfully.'
        }), 200
    
    except Exception as e:
        # Handle errors
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'An error occurred while updating.',
            'error': str(e)
        }), 500
    
# Delete particular employee details
@app.route('/delete_employee/<employee_id>', methods=['DELETE'])
def delete_employee(employee_id):

    # Get employee details by id number
    employee = EmployeeDetails.query.get(employee_id)

    # If employee details are not found
    if not employee:
        return jsonify({
            'success': False,
            'message': 'ID Number does not exist.'
            }), 404
    
    # Delete from database
    try:
        db.session.delete(employee)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Employee details deleted successfully.'
        }), 200
    
    except Exception as e:
        # Handle errors
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'An error occurred while deleting.',
            'error': str(e)
        }), 500
    

    