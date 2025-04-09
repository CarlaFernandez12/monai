import logging
from flask import Flask
from monai.deploy.core import Application
from endpoints.ping_endpoint import ping
from endpoints.upload_endpoint import upload_images
from config import UPLOAD_FOLDER

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
        self.app.add_url_rule('/ping', 'ping', ping, methods=['GET'])
        self.app.add_url_rule('/upload', 'upload_images', upload_images, methods=['POST'])

    def run(self):
        try:
            self.app.run(debug=True, host="0.0.0.0", port=5000)
        except Exception as e:
            logger.error(f"Error al iniciar la aplicación Flask: {str(e)}")
            raise

if __name__ == "__main__":
    app = ImageProcessingApp()
    app.run()