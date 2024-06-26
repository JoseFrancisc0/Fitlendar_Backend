import unittest
import json
from flask import Flask
from flask_testing import TestCase
from ejercicios import ejercicios_api, db, Ejercicio  # Adjust the import based on your file name

class EjercicioAPITestCase(TestCase):
    def create_app(self):
        # Use a test configuration for the Flask application
        ejercicios_api.config['TESTING'] = True
        ejercicios_api.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        ejercicios_api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        return ejercicios_api

    def setUp(self):
        # Create all tables
        db.create_all()

    def tearDown(self):
        # Drop all tables
        db.session.remove()
        db.drop_all()

    def test_get_non_existent_ejercicio(self):
        # Define an ID that does not exist
        non_existent_id = 999

        # Make a GET request to the endpoint
        response = self.client.get(f'/ejercicios/{non_existent_id}')

        # Parse the response data
        data = json.loads(response.data)

        # Assert the response status code and message
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 'Not found.')

    def test_create_ejercicio(self):
        # Define the data for the new ejercicio
        new_ejercicio_data = {
            'nombre': 'Squat',
            'descripcion': 'A basic squat exercise.',
            'dificultad': 'Medium',
            'tipo': 'Strength',
            'equipo': 'None',
            'musculo': 'Legs',
            'peso': 0,
            'series': 3,
            'repeticiones': 12,
            'duracion': 60,
            'foto': 'url_to_photo'
        }

        # Make a POST request to create a new ejercicio
        response = self.client.post('/ejercicios', data=json.dumps(new_ejercicio_data), content_type='application/json')

        # Parse the response data
        data = json.loads(response.data)

        # Assert the response status code and message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Ejercicio created successfully')

        # Verify the new ejercicio is in the database
        ejercicio = Ejercicio.query.filter_by(nombre='Squat').first()
        self.assertIsNotNone(ejercicio)
        self.assertEqual(ejercicio.nombre, 'Squat')
        self.assertEqual(ejercicio.descripcion, 'A basic squat exercise.')
        self.assertEqual(ejercicio.dificultad, 'Medium')
        self.assertEqual(ejercicio.tipo, 'Strength')
        self.assertEqual(ejercicio.equipo, 'None')
        self.assertEqual(ejercicio.musculo, 'Legs')
        self.assertEqual(ejercicio.peso, 0)
        self.assertEqual(ejercicio.series, 3)
        self.assertEqual(ejercicio.repeticiones, 12)
        self.assertEqual(ejercicio.duracion, 60)
        self.assertEqual(ejercicio.foto, 'url_to_photo')

    def test_update_ejercicio(self):
        self.client.post('/ejercicios', json={ #Ejercicio de prueba
            'nombre': 'Squat',
            'descripcion': 'A basic squat exercise.',
            'dificultad': 'Medium',
            'tipo': 'Strength',
            'equipo': 'None',
            'musculo': 'Legs',
            'peso': 0,
            'series': 3,
            'repeticiones': 12,
            'duracion': 60,
            'foto': 'url_to_photo'
        })
        response = self.client.patch('/ejercicios/1', json={
            'nombre': 'Ejercicio Actualizado'
        })
        self.assertEqual(response.status_code, 200) #Ejercicio creado
        self.assertIn('Ejercicio updated successfully', response.get_data(as_text=True))

        # Verifica que el ejercicio se haya actualizado
        response = self.client.get('/ejercicios/1')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['nombre'], 'Ejercicio Actualizado')

    def test_delete_ejercicio(self):
        self.client.post('/ejercicios', json={ #Ejercicio de prueba
            'nombre': 'Squat',
            'descripcion': 'A basic squat exercise.',
            'dificultad': 'Medium',
            'tipo': 'Strength',
            'equipo': 'None',
            'musculo': 'Legs',
            'peso': 0,
            'series': 3,
            'repeticiones': 12,
            'duracion': 60,
            'foto': 'url_to_photo'
        })
        response = self.client.delete('/ejercicios/1')
        self.assertEqual(response.status_code, 200) #Ejercicio creado
        self.assertIn('Ejercicio deleted sucessfully', response.get_data(as_text=True))

        # Verifica que el ejercicio se haya eliminado
        response = self.client.get('/ejercicios/1')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Not found', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
