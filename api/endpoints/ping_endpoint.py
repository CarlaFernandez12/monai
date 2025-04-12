from flask import jsonify

def ping():
    return jsonify({'message': 'The server is working properly'}),200