from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from passlib.hash import scrypt

# Create the application Flask
app = Flask(__name__)

# Configuring SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://auth_user:auth_password@postgres_auth:5432/auth_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Recommended for performance

# Initialize SQLAlchemy with the application (consider a separate file for configuration)
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Assuming hashed password length

# Create all tables (use a context manager for safety, optional outside development)
with app.app_context():
    db.create_all()  # Create tables only if they don't already exist

# Configure JWT
app.config['JWT_SECRET_KEY'] = 'mi-clave-secreta'  # Replace with a strong, random secret key
jwt = JWTManager(app)

# Define routes
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if username is None or password is None:
        return jsonify({'error': 'Missing username or password'}), 400

    user = User.query.filter_by(username=username).first()

    if user is not None:
        return jsonify({'error': 'Username already exists'}), 400

    hashed_password = scrypt.hash(password)  # Use scrypt with salt_length

    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registration successful'}), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if username is None or password is None:
        return jsonify({'error': 'Missing username or password'}), 400

    user = User.query.filter_by(username=username).first()

    if user is None or not scrypt.verify(password, user.password):
        return jsonify({'error': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 200

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({'message': f'Welcome, {current_user}!'})

@app.route('/refresh', methods=['POST'])
@jwt_required()
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify({'access_token': access_token}), 200

# Execute the application Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)  # Consider using a production-ready server in deployment
