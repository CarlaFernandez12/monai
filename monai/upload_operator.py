import os
import requests
import pydicom
from monai.deploy.core import Operator

MONAI_URL = "http://nostalgic_mahavira:5000/upload"
DICOM_FOLDER = "/app/data/uploads"
DOWNLOAD_SUFFIX = "_downloaded.dcm" 

class UploadToMONAIOperator(Operator):
    def init(self, fragment):
        super().init(fragment)

    def compute(self, context):

        dicom_files = [f for f in os.listdir(DICOM_FOLDER) if f.endswith(DOWNLOAD_SUFFIX)]

        if not dicom_files:
            print("❌ No hay archivos DICOM descargados con '_downloaded.dcm' en la carpeta.")
            return

        for dicom_file in dicom_files:
            dicom_path = os.path.join(DICOM_FOLDER, dicom_file)

            try:
                ds = pydicom.dcmread(dicom_path)
                ds.PatientName = getattr(ds, "PatientName", "Test Patient")
                ds.PatientID = getattr(ds, "PatientID", "123456")
                ds.StudyDescription = "Test Study"
                ds.SeriesDescription = "Processed Images"
                ds.StudyInstanceUID = pydicom.uid.generate_uid()
                ds.SeriesInstanceUID = pydicom.uid.generate_uid()

                modified_file_name = f"mod_{dicom_file}"
                modified_path = os.path.join(DICOM_FOLDER, modified_file_name)
                ds.save_as(modified_path)

                if os.path.exists(modified_path):

                    with open(modified_path, "rb") as dicom_file:
                        files = {"file": dicom_file}
                        upload_response = requests.post(MONAI_URL, files=files)

                    if upload_response.status_code == 200:
                        print(f"✅ {modified_file_name} subido con éxito a MONAI Deploy.")
                    else:
                        print(f"❌ Error al subir {modified_file_name}: {upload_response.status_code}, {upload_response.text}")
                else:
                    print(f"❌ El archivo modificado no existe: {modified_path}")

                if os.path.exists(dicom_path):
                    os.remove(dicom_path)
                    print(f"✅ Archivo original eliminado: {dicom_path}")
                else:
                    print(f"❌ No se encontró el archivo original para eliminar: {dicom_path}")

            except Exception as e:
                print(f"❌ Error al procesar {dicom_path}: {e}")