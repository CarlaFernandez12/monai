import os
from flask import request, jsonify
from api.config import UPLOAD_FOLDER
import logging

logger = logging.getLogger(__name__)

def upload_images():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No se encontró ningún archivo en la solicitud'}), 400

        files = request.files.getlist('file')
        saved_files = []

        for file in files:
            if file.filename == '':
                return jsonify({'error': 'Uno de los archivos no tiene un nombre válido'}), 400

            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            saved_files.append(file_path)

        return jsonify({'message': f'{len(saved_files)} archivos subidos correctamente', 'files': saved_files}), 200

    except Exception as e:
        logger.error(f"Error en /upload: {str(e)}")
        return jsonify({'error':str(e)}),500