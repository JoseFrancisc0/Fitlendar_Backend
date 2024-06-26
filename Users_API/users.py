from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

# Instanciar SQLAlchemy
users_api = Flask(__name__)
users_api.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:YAazvWupayIfCP1GWeml@fl-database.clttsra2gi97.us-east-1.rds.amazonaws.com:5432/db-fitlendar"
users_api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(users_api)
CORS(users_api)

# Modelo
class User(db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(100), primary_key = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)
    nombre = db.Column(db.String(100), nullable = False)
    altura = db.Column(db.Numeric(4, 2), nullable = False)
    peso = db.Column(db.Numeric(4, 1), nullable = False)
    foto = db.Column(db.String(255), nullable = False)
    def __repr__(self):
        return f'<User {self.email}>'

# 400 error handler
@users_api.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request.'}), 400

# 404 error handler
@users_api.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found.'}), 404

# 500 error handler
@users_api.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal server error.'}), 500

# Register User
@users_api.route('/users/register', methods = ['POST'])
def register_user():
    data = request.get_json()

    if not data or not 'email' in data or not 'password' in data:
        return bad_request(400)

    if not 'nombre' in data or not 'altura' in data or not 'peso' in data or not 'foto' in data:
        return bad_request(400)
    
    email = data['email']
    password = data['password']
    nombre = data['nombre']
    altura = data['altura']
    peso = data['peso']
    foto = data['foto']

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    new_user = User(email=email, password=hashed_password, nombre=nombre, altura=altura, peso=peso, foto=foto)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User added successfully'}), 200

# Login User
@users_api.route('/users/login', methods = ['POST', 'GET'])
def log_user():
    data = request.get_json()

    if not data or not 'email' in data or not 'password' in data:
        return bad_request(400)
    
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()

    if not user:
        return not_found(404)
    
    if not check_password_hash(user.password, password):
        return jsonify({'error': 'Incorrect password'}), 401
    
    return jsonify({'message': 'Logged in successfully'}), 200

# List User
@users_api.route('/users/<email>', methods = ['GET'])
def get_user(email):
    user = User.query.get(email)

    if user is None:
        return not_found(404)

    return jsonify({'nombre': user.nombre,
                    'altura': user.altura,
                    'peso': user.peso,
                    'foto': user.foto}), 200

# Update User
@users_api.route('/users/<email>', methods = ['PATCH'])
def update_user_profile(email):
    user = User.query.get(email)

    if user is None:
        return not_found(404)

    data = request.get_json()
    if not data:
        return bad_request(400)
    
    if 'nombre' in data:
        user.nombre = data['nombre']
    if 'altura' in data:
        user.altura = data['altura']
    if 'peso' in data:
        user.peso = data['peso']
    if 'foto' in data:
        user.foto = data['foto']

    db.session.commit()

    return jsonify({'message': 'User updated successfully'}), 200
    
# Run
if __name__ == '__main__':
    users_api.run(host = '0.0.0.0', port = 8002, debug = True)
