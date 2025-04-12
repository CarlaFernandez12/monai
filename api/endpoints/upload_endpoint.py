import os
from flask import request, jsonify
from config import UPLOAD_FOLDER
import logging

logger = logging.getLogger(__name__)

def upload_images():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file was found in the request'}), 400

        files = request.files.getlist('file')
        saved_files = []

        for file in files:
            if file.filename == '':
                return jsonify({'error': 'One of the files does not have a valid name'}), 400

            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            saved_files.append(file_path)

        return jsonify({'message': f'{len(saved_files)} files upload properly', 'files': saved_files}), 200

    except Exception as e:
        logger.error(f"Error /upload: {str(e)}")
        return jsonify({'error':str(e)}),500