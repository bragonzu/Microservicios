from flask import Flask, jsonify, request,render_template
import requests
app = Flask(__name__)

# Middleware de autenticación
def autenticar_usuario():
    return True

@app.route('/servicio_protegido', methods=['GET'])
def servicio_protegido():
    if not autenticar_usuario():
        return jsonify({'error': 'Autenticación fallida'}), 401
    
    
    return jsonify({'mensaje': 'Acceso concedido al servicio protegido'}), 200


@app.route('/')
def index():
    return render_template('api_gateway.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
