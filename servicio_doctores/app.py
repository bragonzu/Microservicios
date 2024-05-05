from flask import Flask, jsonify, request

app = Flask(__name__)

# Datos de doctores de ejemplo
doctores = [
    {'id': 1, 'nombre': 'Doctor 1', 'especialidad': 'Pediatra'},
    {'id': 2, 'nombre': 'Doctor 2', 'especialidad': 'Cardiólogo'},
    {'id': 3, 'nombre': 'Doctor 3', 'especialidad': 'Dermatólogo'}
]
next_id = 4  # ID para el próximo doctor

# Ruta para obtener todos los doctores
@app.route('/doctores', methods=['GET'])
def obtener_doctores():
    return jsonify(doctores)

# Ruta para obtener un doctor por su ID
@app.route('/doctores/<int:doctor_id>', methods=['GET'])
def obtener_doctor(doctor_id):
    doctor = next((doctor for doctor in doctores if doctor['id'] == doctor_id), None)
    if doctor:
        return jsonify(doctor)
    else:
        return jsonify({'error': 'Doctor no encontrado'}), 404

# Ruta para crear un nuevo doctor
@app.route('/doctores', methods=['POST'])
def crear_doctor():
    global next_id
    nuevo_doctor = {
        'id': next_id,
        'nombre': request.json.get('nombre', ''),
        'especialidad': request.json.get('especialidad', '')
    }
    doctores.append(nuevo_doctor)
    next_id += 1
    return jsonify(nuevo_doctor), 201

# Ruta para actualizar un doctor existente por su ID
@app.route('/doctores/<int:doctor_id>', methods=['PUT'])
def actualizar_doctor(doctor_id):
    doctor = next((doctor for doctor in doctores if doctor['id'] == doctor_id), None)
    if doctor:
        doctor['nombre'] = request.json.get('nombre', doctor['nombre'])
        doctor['especialidad'] = request.json.get('especialidad', doctor['especialidad'])
        return jsonify(doctor)
    else:
        return jsonify({'error': 'Doctor no encontrado'}), 404

# Ruta para eliminar un doctor existente por su ID
@app.route('/doctores/<int:doctor_id>', methods=['DELETE'])
def eliminar_doctor(doctor_id):
    global doctores
    doctores = [doctor for doctor in doctores if doctor['id'] != doctor_id]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
