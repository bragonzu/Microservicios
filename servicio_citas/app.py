from flask import Flask, jsonify, request,render_template

app = Flask(__name__)

# Datos de citas de ejemplo
citas = [
    {'id': 1, 'paciente': 'Paciente 1', 'fecha': '2024-05-05'},
    {'id': 2, 'paciente': 'Paciente 2', 'fecha': '2024-05-06'},
    {'id': 3, 'paciente': 'Paciente 3', 'fecha': '2024-05-07'}
]
next_id = 4  # ID para la próxima cita

# Ruta para obtener todas las citas
@app.route('/citas', methods=['GET'])
def obtener_citas():
    return jsonify(citas)

# Ruta para obtener una cita por su ID
@app.route('/citas/<int:cita_id>', methods=['GET'])
def obtener_cita(cita_id):
    cita = next((cita for cita in citas if cita['id'] == cita_id), None)
    if cita:
        return jsonify(cita)
    else:
        return jsonify({'error': 'Cita no encontrada'}), 404

# Ruta para crear una nueva cita
@app.route('/citas', methods=['POST'])
def crear_cita():
    global next_id
    nueva_cita = {
        'id': next_id,
        'paciente': request.json.get('paciente', ''),
        'fecha': request.json.get('fecha', '')
    }
    citas.append(nueva_cita)
    next_id += 1
    return jsonify(nueva_cita), 201

# Ruta para actualizar una cita existente por su ID
@app.route('/citas/<int:cita_id>', methods=['PUT'])
def actualizar_cita(cita_id):
    cita = next((cita for cita in citas if cita['id'] == cita_id), None)
    if cita:
        cita['paciente'] = request.json.get('paciente', cita['paciente'])
        cita['fecha'] = request.json.get('fecha', cita['fecha'])
        return jsonify(cita)
    else:
        return jsonify({'error': 'Cita no encontrada'}), 404

# Ruta para eliminar una cita existente por su ID
@app.route('/citas/<int:cita_id>', methods=['DELETE'])
def eliminar_cita(cita_id):
    global citas
    citas = [cita for cita in citas if cita['id'] != cita_id]
    return '', 204

@app.route('/servicio_citas')
def citas():
    return render_template('cita.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
