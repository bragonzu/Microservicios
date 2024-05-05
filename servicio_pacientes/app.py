from flask import Flask, jsonify, request

app = Flask(__name__, template_folder='shared_templates')

# Datos de pacientes de ejemplo
pacientes = [
    {'id': 1, 'nombre': 'Paciente 1', 'edad': 30},
    {'id': 2, 'nombre': 'Paciente 2', 'edad': 35},
    {'id': 3, 'nombre': 'Paciente 3', 'edad': 40}
]
next_id = 4  # ID para el próximo paciente

# Ruta para obtener todos los pacientes
@app.route('/pacientes', methods=['GET'])
def obtener_pacientes():
    return jsonify(pacientes)

# Ruta para obtener un paciente por su ID
@app.route('/pacientes/<int:paciente_id>', methods=['GET'])
def obtener_paciente(paciente_id):
    paciente = next((paciente for paciente in pacientes if paciente['id'] == paciente_id), None)
    if paciente:
        return jsonify(paciente)
    else:
        return jsonify({'error': 'Paciente no encontrado'}), 404

# Ruta para crear un nuevo paciente
@app.route('/pacientes', methods=['POST'])
def crear_paciente():
    global next_id
    nuevo_paciente = {
        'id': next_id,
        'nombre': request.json.get('nombre', ''),
        'edad': request.json.get('edad', 0)
    }
    pacientes.append(nuevo_paciente)
    next_id += 1
    return jsonify(nuevo_paciente), 201

# Ruta para actualizar un paciente existente por su ID
@app.route('/pacientes/<int:paciente_id>', methods=['PUT'])
def actualizar_paciente(paciente_id):
    paciente = next((paciente for paciente in pacientes if paciente['id'] == paciente_id), None)
    if paciente:
        paciente['nombre'] = request.json.get('nombre', paciente['nombre'])
        paciente['edad'] = request.json.get('edad', paciente['edad'])
        return jsonify(paciente)
    else:
        return jsonify({'error': 'Paciente no encontrado'}), 404

# Ruta para eliminar un paciente existente por su ID
@app.route('/pacientes/<int:paciente_id>', methods=['DELETE'])
def eliminar_paciente(paciente_id):
    global pacientes
    pacientes = [paciente for paciente in pacientes if paciente['id'] != paciente_id]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
