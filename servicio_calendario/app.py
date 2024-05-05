from flask import Flask, jsonify, request
from werkzeug.urls import quote

app = Flask(__name__)

# Datos de eventos del calendario de ejemplo
eventos = [
    {'id': 1, 'titulo': 'Reunión de equipo', 'fecha': '2024-05-10', 'hora': '10:00'},
    {'id': 2, 'titulo': 'Cita médica', 'fecha': '2024-05-12', 'hora': '15:30'},
    {'id': 3, 'titulo': 'Conferencia', 'fecha': '2024-05-15', 'hora': '09:00'}
]
next_id = 4  # ID para el próximo evento

# Ruta para obtener todos los eventos del calendario
@app.route('/eventos', methods=['GET'])
def obtener_eventos():
    return jsonify(eventos)

# Ruta para obtener un evento del calendario por su ID
@app.route('/eventos/<int:evento_id>', methods=['GET'])
def obtener_evento(evento_id):
    evento = next((evento for evento in eventos if evento['id'] == evento_id), None)
    if evento:
        return jsonify(evento)
    else:
        return jsonify({'error': 'Evento no encontrado'}), 404

# Ruta para crear un nuevo evento en el calendario
@app.route('/eventos', methods=['POST'])
def crear_evento():
    global next_id
    nuevo_evento = {
        'id': next_id,
        'titulo': request.json.get('titulo', ''),
        'fecha': request.json.get('fecha', ''),
        'hora': request.json.get('hora', '')
    }
    eventos.append(nuevo_evento)
    next_id += 1
    return jsonify(nuevo_evento), 201

# Ruta para actualizar un evento existente en el calendario por su ID
@app.route('/eventos/<int:evento_id>', methods=['PUT'])
def actualizar_evento(evento_id):
    evento = next((evento for evento in eventos if evento['id'] == evento_id), None)
    if evento:
        evento['titulo'] = request.json.get('titulo', evento['titulo'])
        evento['fecha'] = request.json.get('fecha', evento['fecha'])
        evento['hora'] = request.json.get('hora', evento['hora'])
        return jsonify(evento)
    else:
        return jsonify({'error': 'Evento no encontrado'}), 404

# Ruta para eliminar un evento existente en el calendario por su ID
@app.route('/eventos/<int:evento_id>', methods=['DELETE'])
def eliminar_evento(evento_id):
    global eventos
    eventos = [evento for evento in eventos if evento['id'] != evento_id]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
