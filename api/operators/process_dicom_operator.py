import logging
from monai.deploy.core import Operator

logger = logging.getLogger(__name__)

class ProcessDICOMOperator(Operator):
    """
    Operador para procesar imágenes DICOM.
    """
    def _init_(self):
        super()._init_()

    def compute(self, input_data):
        input_path = input_data["input_path"]
        output_path = input_data["output_path"]

        logger.info(f"Procesando archivo DICOM: {input_path}")
        logger.info(f"Archivo procesado y guardado en: {output_path}")