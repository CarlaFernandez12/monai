from flask import jsonify

def ping():
    return jsonify({'message': 'El servidor funciona correctamente'}),200