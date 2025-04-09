import os
from orthanc.orthanc_client import OrthancClient

DICOM_FOLDER = "/app/data/uploads"

class SendToOrthancOperator:
    def __init__(self):
        self.orthanc_client = OrthancClient()

    def compute(self):
        print("🚀 Ejecutando SendToOrthancOperator...")
        dicom_files = [f for f in os.listdir(DICOM_FOLDER) if f.endswith(".dcm")]
        
        if not dicom_files:
            print("❌ No hay archivos DICOM en la carpeta.")
            return

        for dicom_file in dicom_files:
            dicom_path = os.path.join(DICOM_FOLDER, dicom_file)
            print(f"📤 Subiendo {dicom_path} a Orthanc...")
            self.orthanc_client.upload_dicom(dicom_path)
            os.remove(dicom_path)
            print(f"🗑 Eliminado original: {dicom_path}")

if __name__ == "__main__":
    operator = SendToOrthancOperator()
    operator.compute()