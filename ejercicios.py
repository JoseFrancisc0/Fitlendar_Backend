from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Instanciar SQLAlchemy
ejercicios_api = Flask(__name__)
ejercicios_api.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://masterdaster:fzUfbTNzduUa2XaJi3rq@db-fitlendar.cjiqbpllrpor.us-east-1.rds.amazonaws.com:5432/db-fitlendar"
ejercicios_api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(ejercicios_api)
CORS(ejercicios_api)

# Modelo
class Ejercicio(db.Model):
    __tablename__ = 'ejercicios'
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    nombre = db.Column(db.String(50), nullable = False)
    repeticiones = db.Column(db.Integer, nullable = False)
    series = db.Column(db.Integer, nullable = False)
    musculo = db.Column(db.String(50), nullable = False)
    icono = db.Column(db.String(200), nullable = False)
    video_ejemplo = db.Column(db.String(200), nullable = False)
    def __repr__(self):
        return f'<Ejercicio {self.id}>'

# 400 error handler
@ejercicios_api.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request.'}), 400

# 404 error handler
@ejercicios_api.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found.'}), 404

# 500 error handler
@ejercicios_api.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal server error.'}), 500

# CREATE API Endpoint
@ejercicios_api.route('/ejercicios', methods = ['POST'])
def create_ejercicio():
    data = request.get_json()

    ejercicio = Ejercicio(
        nombre = data['nombre'],
        repeticiones = data['repeticiones'],
        series = data['series'],
        musculo = data['musculo'],
        icono = data['icono'],
        video_ejemplo = data['video_ejemplo']
    )

    db.session.add(ejercicio)
    db.session.commit()
    
    return jsonify({'message': 'Car created successfully'}), 200

# READ (all) API Endpoint
@ejercicios_api.route('/ejercicios', methods = ['GET'])
def get_ejercicios():
    ejercicios = Ejercicio.query.all()

    return jsonify([{'id' : ejercicio.id,
                     'nombre' : ejercicio.nombre,
                     'repeticiones' : ejercicio.repeticiones,
                     'series' : ejercicio.series,
                     'musculo' : ejercicio.musculo,
                     'icono' : ejercicio.icono,
                     'video_ejemplo' : ejercicio.video_ejemplo
                     } for ejercicio in ejercicios]), 200

# READ (each) API Endpoint
@ejercicios_api.route('/ejercicios/<int:id>', methods = ['GET'])
def get_ejercicio(id):
    ejercicio = Ejercicio.query.get(id)

    if ejercicio is None:
        return not_found(404)
    
    return jsonify({'id' : ejercicio.id,
                     'nombre' : ejercicio.nombre,
                     'repeticiones' : ejercicio.repeticiones,
                     'series' : ejercicio.series,
                     'musculo' : ejercicio.musculo,
                     'icono' : ejercicio.icono,
                     'video_ejemplo' : ejercicio.video_ejemplo}), 200

# UPDATE API Endpoint
@ejercicios_api.route('/ejercicios/<int:id>', methods = ['PATCH'])
def patch_ejercicio(id):
    ejercicio = Ejercicio.query.get(id)
    if ejercicio is None:
        return not_found(404)
    
    data = request.get_json()
    if not data:
        return bad_request(400)

    if 'nombre' in data:
        ejercicio.nombre = data['nombre']
    if 'series' in data:
        ejercicio.series = data['series']
    if 'repeticiones' in data:
        ejercicio.repeticiones = data['repeticiones']
    if 'musculo' in data:
        ejercicio.musculo = data['musculo']
    if 'icono' in data:
        ejercicio.icono = data['icono']
    if 'video_ejemplo' in data:
        ejercicio.video_ejemplo = data['video_ejemplo']

    db.session.commit()

    return jsonify({'message' : 'Ejercicio updated successfully'}), 200

# DELETE API Endpoint
@ejercicios_api.route('/ejercicios/<int:id>', methods = ['DELETE'])
def delete_ejercicio(id):
    ejercicio = Ejercicio.query.get(id)
    if ejercicio is None:
        return not_found(404)
    
    db.session.delete(ejercicio)
    db.session.commit()

    return jsonify({'message': 'Ejercicio deleted sucessfully'}), 200
    
# Run
if __name__ == '__main__':
    ejercicios_api.run(host = '0.0.0.0', port = 8000, debug = True)
