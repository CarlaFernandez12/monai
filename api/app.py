import os
import logging
from flask import Flask, request, jsonify, send_file
from monai.deploy.core import Application
from api.download_endpoint import download_bp
from api.operators.process_dicom_operator import ProcessDICOMOperator


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "uploads"))
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class ImageProcessingApp(Application):
    """
    Aplicación MONAI Deploy para manejar el servidor Flask y procesamiento DICOM.
    """
    def __init__(self):  
        super().__init__()
        self.app = Flask(__name__)
        self.setup_endpoints()

    def compose(self):
        logger.info("Método compose implementado correctamente.")

    def setup_endpoints(self):
        @self.app.route('/ping', methods=['GET'])
        def ping():
            return jsonify({'message': 'El servidor funciona correctamente'}), 200

        @self.app.route('/upload', methods=['POST'])
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
                return jsonify({'error': str(e)}), 500
            
        self.app.register_blueprint(download_bp)

    def run(self):
        try:
            self.app.run(debug=True, host="0.0.0.0", port=5000)
        except Exception as e:
            logger.error(f"Error al iniciar la aplicación Flask: {str(e)}")
            raise
    
            

if __name__ == "__main__":
    app = ImageProcessingApp()
    app.run()
