from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from datetime import datetime, timedelta
import requests  # Import requests library

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://citas_user:citas_password@postgres_citas:5432/citas_database' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
jwt = JWTManager(app)


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    # address = db.Column(db.String(255))

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    specialty = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    notes = db.Column(db.Text)

    patient = db.relationship('Patient', backref='appointments')
    doctor = db.relationship('Doctor', backref='appointments')


# Create the tables (consider a context manager for safety, optional outside development)
# with app.app_context():
#     db.create_all() 



# ... (Your existing routes for appointments and user authentication) ...
AUTH_SERVICE_URL = "http://0.0.0.0:5000"  # Replace with your actual URL and port

def get_access_token(username, password):
    auth_service_url = "http://<auth_service_host>:<auth_service_port>/login"  # Replace with actual URL and port
    data = {
        "username": username,
        "password": password
    }

    response = requests.post(auth_service_url, json=data)

    if response.status_code == 200:
        response_data = response.json()
        return response_data.get("access_token")  # Extract access token from response
    else:
        # Handle login failure (e.g., raise exception, display error message)
        raise Exception("Login failed!")
# Function to validate JWT token
def validate_jwt(jwt_token):
    # Send a POST request to the authentication service's '/validate-jwt' endpoint
    # Include the JWT token in the request body
    # Parse the JSON response and check the 'message' field for validation status
    response = requests.post(AUTH_SERVICE_URL + '/validate-jwt', json={'token': jwt_token})
    if response.status_code == 200:
        response_data = response.json()
        if response_data['message'] == 'Valid JWT':
            return True
        else:
            return False
    else:
        return False

def extract_user_id_from_jwt(jwt_token):
    """Extracts the user ID from a JWT token.

    Args:
        jwt_token (str): The JWT token string.

    Returns:
        int: The user ID extracted from the 'user_id' claim, or None if invalid.

    Raises:
        Exception: If there's an error decoding the JWT.
    """

    try:
        # Replace 'SECRET_KEY' with your actual secret key from the authentication service
        decoded_payload = jwt.decode(jwt_token, 'mi-clave-secreta', algorithms=['HS256'])
        return decoded_payload.get('user_id')  # Extract user ID from the 'user_id' claim
    except jwt.exceptions.DecodeError as e:
        raise Exception(f"Invalid JWT token: {e}")
    

@app.route('/appointment', methods=['POST'])
def create_appointment():
    # Validate appointment details (date, time, doctor availability, etc.)
    # ...

    # Validate and extract user ID from JWT
    if not validate_jwt(request.headers['Authorization']):
        return jsonify({'error': 'Invalid JWT'}), 401

    user_id = extract_user_id_from_jwt(request.headers['Authorization'])

    # Create appointment record using user_id
    new_appointment = Appointment(
        patient_id=user_id,  # Use the extracted user ID
        doctor_id=request.json['doctor_id'],
        date=request.json['date'],
        time=request.json['time'],
        notes=request.json.get('notes')  # Optional notes
    )
    db.session.add(new_appointment)
    db.session.commit()

    return jsonify({'message': 'Appointment created successfully'}), 201


@app.route('/patient', methods=['POST'])
@jwt_required()  # Protect the route with JWT authentication
def create_patient():
    # Validate required fields
    required_fields = ['name', 'email', 'phone']
    if any(field not in request.json for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    # Retrieve user ID from validated JWT
    user_id = get_jwt_identity()

    # Validate access token (optional, consider server-side validation)
    if not validate_jwt(request.headers['Authorization']):  # Check for valid JWT in Authorization header
        return jsonify({'error': 'Invalid JWT'}), 401

    # Create new patient
    new_patient = Patient(
        name=request.json['name'],
        email=request.json['email'],
        phone=request.json['phone'],
        address=request.json.get('address')  # Optional address
    )
    db.session.add(new_patient)
    db.session.commit()

    return jsonify({'message': 'Patient created successfully'}), 201


@app.route('/patient/<int:patient_id>', methods=['GET'])
def get_patient_by_id(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    patient_data = {
        'id': patient.id,
        'name': patient.name,
        'email': patient.email,
        'phone': patient.phone,
        'address': patient.address  # Optional address
    }

    return jsonify(patient_data)

@app.route('/patient/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    # Validate and update patient information
    updated_fields = {key: value for key, value in request.json.items() if key in ['name', 'email', 'phone', 'address']}
    if updated_fields:
        for key, value in updated_fields.items():
            setattr(patient, key, value)

    db.session.commit()
    return jsonify({'message': 'Patient updated successfully'}), 200

@app.route('/doctor', methods=['POST'])
def create_doctor():
    # Validate required fields
    required_fields = ['name', 'specialty', 'email', 'phone']
    if any(field not in request.json for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    # Create new doctor
    new_doctor = Doctor(
        name=request.json['name'],
        specialty=request.json['specialty'],
        email=request.json['email'],
        phone=request.json['phone']
    )
    db.session.add(new_doctor)
    db.session.commit()

    return jsonify({'message': 'Doctor created successfully'}), 201

@app.route('/doctor/<int:doctor_id>', methods=['GET'])
def get_doctor_by_id(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    doctor_data = {
        'id': doctor.id,
        'name': doctor.name,
        'specialty': doctor.specialty,
        'email': doctor.email,
        'phone': doctor.phone
    }

    return jsonify(doctor_data)

@app.route('/doctor/<int:doctor_id>/appointments', methods=['GET'])
def get_appointments_by_doctor(doctor_id):
    appointments = Appointment.query.filter_by(doctor_id=doctor_id).all()
    appointment_data = []

    for appointment in appointments:
        appointment_data.append({
            'id': appointment.id,
            'patient_id': appointment.patient_id,
            'date': appointment.date.strftime('%Y-%m-%d'),
            'time': appointment.time.strftime('%H:%M:%S'),
            'notes': appointment.notes
        })

    return jsonify({'appointments': appointment_data})


@app.route('/patient/<int:patient_id>/appointments', methods=['GET'])
def get_appointments_by_patient_id(patient_id):
    # Validate patient ID
    patient = Patient.query.get_or_404(patient_id)

    # Retrieve appointments for the patient
    appointments = patient.appointments

    # Convert appointments into a list of dictionaries with relevant information
    appointment_data = []
    for appointment in appointments:
        appointment_data.append({
            'appointment_id': appointment.id,
            'doctor_name': appointment.doctor.name,
            'date': appointment.date.strftime('%Y-%m-%d'),
            'time': appointment.time.strftime('%H:%M:%S'),
            'notes': appointment.notes
        })

    return jsonify({'appointments': appointment_data}), 200

if __name__ == '__main__':
    app.run(host='localhost', debug=True)
