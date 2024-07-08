from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta, time

# Instanciar SQLAlchemy
horarios_api = Flask(__name__)
horarios_api.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:MdMtX9piRNif172H2jq4@database-fitlendar.cjiqbpllrpor.us-east-1.rds.amazonaws.com:5432/postgres"
horarios_api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(horarios_api)
CORS(horarios_api)

# Modelos
class Ejercicio(db.Model):
    __tablename__ = 'ejercicios'
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    nombre = db.Column(db.String(50), nullable = False)
    descripcion = db.Column(db.String(300), nullable = False)
    dificultad = db.Column(db.String(20), nullable = False)
    tipo = db.Column(db.String(20), nullable = False)
    equipo = db.Column(db.String(50), nullable = False)
    musculo = db.Column(db.String(50), nullable = False)
    peso = db.Column(db.Integer, nullable = False)
    series = db.Column(db.Integer, nullable = False)
    repeticiones = db.Column(db.Integer, nullable = False)
    calorias = db.Column(db.Integer, nullable = False)
    duracion = db.Column(db.Integer, nullable = False)
    foto = db.Column(db.String(255), nullable = False)
    
    def __repr__(self):
        return f'<Ejercicio {self.id}>'

class User(db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(100), primary_key = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)
    nombre = db.Column(db.String(100), nullable = False)
    altura = db.Column(db.Numeric(4, 2), nullable = False)
    peso = db.Column(db.Numeric(4, 1), nullable = False)
    foto = db.Column(db.String(255), nullable = False)
    racha = db.Column(db.Integer, nullable = False)
    calorias_quemadas = db.Column(db.Integer, nullable = False)
    logueado = db.Column(db.Boolean, nullable = False)
    def __repr__(self):
        return f'<User {self.email}>'

class Horario(db.Model):
    __tablename__ = 'horarios'
    user_email = db.Column(db.String(100), db.ForeignKey('users.email'), primary_key=True, nullable=False)
    ejercicio_id = db.Column(db.Integer, db.ForeignKey('ejercicios.id'), nullable=False)
    fecha = db.Column(db.Date, primary_key=True, nullable=False)
    inicio = db.Column(db.Time, primary_key=True, nullable=False)
    fin = db.Column(db.Time, primary_key=True, nullable=False)
    completed = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<Horario: {self.user_email}, {self.horario}>'

# 400 error handler
@horarios_api.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request.'}), 400

# 404 error handler
@horarios_api.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found.'}), 404

# Create Horario
@horarios_api.route('/horarios', methods=['POST'])
def create_horario():
    data = request.get_json()

    if data is None:
        return bad_request(400)

    fecha = datetime.strptime(data['fecha'], '%Y-%m-%d').date()
    inicio = datetime.strptime(data['inicio'], '%H:%M').time()

    ejercicio = Ejercicio.query.get(data['ejercicio_id'])
    if ejercicio is None:
        return not_fount(404)
    
    h, m = divmod(ejercicio.duracion, 60)
    f_h = inicio.hour + h
    f_m = inicio.minute + m
    
    if f_m > 60:
        f_h += 1
        f_m %= 60
        
    f_h %= 24
    fin = time(hour=f_h, minute=f_m)
    
    horario = Horario(
        user_email = data['user_email'],
        ejercicio_id = data['ejercicio_id'],
        fecha = fecha,
        inicio = inicio,
        fin = fin,
        completed = False
    )

    db.session.add(horario)
    db.session.commit()

    return jsonify({'message' : 'Horario created successfully'}), 200

# Read Horarios
@horarios_api.route('/horarios/<user_email>', methods=['GET'])
def get_horarios(user_email):
    horarios = Horario.query.filter_by(user_email=user_email).all()

    return jsonify([{'user_email' : horario.user_email,
                     'ejercicio_id' : horario.ejercicio_id,
                     'fecha' : horario.fecha.isoformat(),
                     'inicio' : horario.inicio.isoformat(),
                     'fin' : horario.fin.isoformat(),
                     'completed' : horario.completed
                     } for horario in horarios]), 200

# Update Horario
@horarios_api.route('/horarios/<user_email>', methods=['PATCH'])
def update_horario(user_email, horario):
    # Json payload
    data = request.get_json()
    if data is None:
        return bad_request(400)
    if 'fecha' not in data['fecha'] or 'inicio' not in data['inicio']:
        return bad_request(400)

    fecha = datetime.strptime(data['fecha'], '%Y-%m-%d').date()
    inicio = datetime.strptime(data['inicio'], '%H:%M').time()

    # Search horario
    h = Horario.query.filter_by(user_email=user_email, fecha=fecha, inicio=inicio).first()
    if h is None:
        return not_found(404)

    h.completed = True # Flag completed

    ejercicio = Ejercicio.query.get(h.ejercicio_id)
    if ejercicio is None:
        return not_found(404)

    user = User.query.get(h.user_email)
    if user is None:
        return not_found(404)
    user.calorias_quemadas += ejercicio.calorias # Update calorias

    check_racha = Horario.query.filter_by(user_email=h.user_email, fecha=h.fecha).first()
    if check_racha is None:
        user.racha += 1 # Update racha
                
    db.session.commit()
    
    return jsonify({'message': 'Horario updated successfully'}), 200

# Delete Horario
@horarios_api.route('/horarios/<user_email>/<horario>', methods=['DELETE'])
def delete_horario(user_email, horario):
    h = Horario.query.filter_by(user_email=user_email, horario=horario).first()
    if h is None:
        return not_found(404)
    
    db.session.delete(h)
    db.session.commit()

    return jsonify({'message': 'Horario deleted successfully'}), 200

# Run
if __name__ == '__main__':
    horarios_api.run(host = '0.0.0.0', port = 8003, debug = True)
