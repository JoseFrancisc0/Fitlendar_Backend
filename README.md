# Fitlendar_Backend

## Roadmap

API: Ejercicios, Horarios, Metas

### API_Ejercicios

- Comunica con la db ejercicios
- Fetchea la data de cada ejercicio q tengamos en la app
- Nuestra app deberia leer lista de ejercicios get_exercise_list()
- Deberia tambien un add_custom_exercise(), va a local

### API Horarios

- Fecha + Hora + Ejercicio
- Deberia comunicar la app con Google Calendar (si es q esta linkeado)
- Escribir eventos de Google Calendar (Horario) usando los ejercicios de API_ejercicios
- Si no esta linkeado, deberia guardarse en local (de alguna forma)
- Queda buscar como identificar nuestros eventos

- Local: guardar_evento_local()
- Google: mandar_google() de primeras, despues escribimos eventos en Google Calendar

### Metas

- Revisa Horarios con (completed: True)
- Un usuario tiene su lista de metas
- Usa datos de perfil, con su horario
- Entonces se escribe a perfil
- Datos de usuario lo manejamos con Google
- Si no esta linkeado, esta guardado en local
- Metas --> datos de usario.
*** Metas no es API

## DONE
- Plantilla de API_ejercicios usando flask
- Base de datos con DynamoDB

## TODO
- Acomodar la API_ejercicios de SQL a NoSQL
- Convertir metodos a funciones lambda
- Unir las funciones bajo APIGateway
- Testing (?)
