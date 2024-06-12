from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

# Instanciar SQLAlchemy
users_api = Flask(__name__)
users_api.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://masterdaster:fzUfbTNzduUa2XaJi3rq@db-fitlendar.cjiqbpllrpor.us-east-1.rds.amazonaws.com:5432/db-fitlendar"
users_api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(users_api)
CORS(users_api)

# Modelo
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    email = db.Column(db.String(100), nullable = False)
    password = db.Column(db.String(100), nullable = False)
    def __repr__(self):
        return f'<User {self.id}>'

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

    email = data['email']
    password = data['password']

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    hashed_password = generate_password_hash(password, method='sha256')

    new_user = User(email=email, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message: User added successfully'}), 200

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

# Run
if __name__ == '__main__':
    users_api.run(host = '0.0.0.0', port = 8002, debug = True)
