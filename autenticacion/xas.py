# # from flask import Flask, jsonify, request
# # from flask_cors import CORS
# # from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token, create_refresh_token
# # from werkzeug.security import generate_password_hash, check_password_hash
# # from flask_sqlalchemy import SQLAlchemy

# # app = Flask(__name__)
# # CORS(app)
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://auth_user:auth_password@postgres:5432/auth_database'
# # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# # app.config['JWT_SECRET_KEY'] = 'mi-clave-secreta'

# # db = SQLAlchemy(app)
# # jwt = JWTManager(app)

# # # Definir el modelo de usuario
# # class User(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     username = db.Column(db.String(80), unique=True, nullable=False)
# #     password = db.Column(db.String(128), nullable=False)

# #     def __repr__(self):
# #         return f'<User {self.username}>'

# # # Registro de usuario
# # @app.route('/register', methods=['POST'])
# # def register():
# #     data = request.json
# #     username = data.get('username')
# #     password = data.get('password')

# #     if not username or not password:
# #         return jsonify({'error': 'Missing username or password'}), 400

# #     if User.query.filter_by(username=username).first():
# #         return jsonify({'error': 'Username already exists'}), 400

# #     hashed_password = generate_password_hash(password)
# #     new_user = User(username=username, password=hashed_password)
# #     db.session.add(new_user)
# #     db.session.commit()

# #     return jsonify({'message': 'User registration successful'}), 201

# # # Inicio de sesión de usuario
# # @app.route('/login', methods=['POST'])
# # def login():
# #     data = request.json
# #     username = data.get('username')
# #     password = data.get('password')

# #     if not username or not password:
# #         return jsonify({'error': 'Missing username or password'}), 400

# #     user = User.query.filter_by(username=username).first()

# #     if not user or not check_password_hash(user.password, password):
# #         return jsonify({'error': 'Invalid username or password'}), 401

# #     access_token = create_access_token(identity=user.id)
# #     refresh_token = create_refresh_token(identity=user.id)

# #     return jsonify({
# #         'access_token': access_token,
# #         'refresh_token': refresh_token
# #     }), 200

# # # Ruta protegida
# # @app.route('/protected', methods=['GET'])
# # @jwt_required()
# # def protected():
# #     current_user_id = get_jwt_identity()
# #     user = User.query.get(current_user_id)
# #     return jsonify({'username': user.username}), 200

# # # Actualización de tokens de acceso
# # @app.route('/refresh', methods=['POST'])
# # @jwt_required(refresh=True)
# # def refresh():
# #     current_user_id = get_jwt_identity()
# #     access_token = create_access_token(identity=current_user_id)
# #     return jsonify({'access_token': access_token}), 200

# # if __name__ == '__main__':
# #     app.run(debug=True, port=5000)
# from flask import Flask, jsonify, request
# from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token, create_refresh_token
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://auth_user:auth_password@postgres:5432/auth_database'  # Actualiza esta URL
# app.config['JWT_SECRET_KEY'] = 'mi-clave-secreta'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactiva el seguimiento de modificaciones de SQLAlchemy
# db = SQLAlchemy(app)
# jwt = JWTManager(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String(128), nullable=False)

# @app.route('/register', methods=['POST'])
# def register():
#     username = request.json.get('username')
#     password = request.json.get('password')

#     if username is None or password is None:
#         return jsonify({'error': 'Missing username or password'}), 400

#     user = User.query.filter_by(username=username).first()

#     if user is not None:
#         return jsonify({'error': 'Username already exists'}), 400

#     hashed_password = generate_password_hash(password)
#     new_user = User(username=username, password=hashed_password)
#     db.session.add(new_user)
#     db.session.commit()

#     return jsonify({'message': 'User registration successful'}), 201

# @app.route('/login', methods=['POST'])
# def login():
#     username = request.json.get('username')
#     password = request.json.get('password')

#     if username is None or password is None:
#         return jsonify({'error': 'Missing username or password'}), 400

#     user = User.query.filter_by(username=username).first()

#     if user is None or not check_password_hash(user.password, password):
#         return jsonify({'error': 'Invalid username or password'}), 401

#     access_token = create_access_token(identity=username)
#     refresh_token = create_refresh_token(identity=username)

#     return jsonify({
#         'access_token': access_token,
#         'refresh_token': refresh_token
#     }), 200

# @app.route('/protected', methods=['GET'])
# @jwt_required()
# def protected():
#     current_user = get_jwt_identity()
#     return jsonify({'message': f'Welcome, {current_user}!'})

# @app.route('/refresh', methods=['POST'])
# def refresh():
#     current_user = get_jwt_identity()
#     access_token = create_access_token(identity=current_user)
#     return jsonify({'access_token': access_token}), 200

# if __name__ == '__main__':
#     db.create_all()
#     app.run(host='0.0.0.0', debug=True)  # Ejecutar la aplicación en todas las interfaces de red
