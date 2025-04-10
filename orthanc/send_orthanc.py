import os
from orthanc.orthanc_client import OrthancClient
from utils.file_utils import list_dicom_files, remove_file

DICOM_FOLDER = "/app/data/uploads"


def process_dicom_file(client: OrthancClient, file_path: str):
    print(f"📤 Subiendo {file_path} a Orthanc...")
    client.upload_dicom(file_path)
    remove_file(file_path)
    print(f"🗑 Eliminado original: {file_path}")


class SendToOrthancOperator:
    def __init__(self, folder: str = DICOM_FOLDER): 
        self.orthanc_client = OrthancClient()
        self.folder = folder

    def compute(self):
        print("🚀 Ejecutando SendToOrthancOperator...")
        dicom_files = list_dicom_files(self.folder)

        if not dicom_files:
            print("❌ No hay archivos DICOM en la carpeta.")
            return

        for file_name in dicom_files:
            file_path = os.path.join(self.folder, file_name)
            process_dicom_file(self.orthanc_client, file_path)


if __name__ == "__main__":  
    SendToOrthancOperator().compute()