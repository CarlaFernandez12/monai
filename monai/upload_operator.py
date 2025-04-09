import os
import requests
import pydicom
from typing import List
from monai.deploy.core import Operator

MONAI_URL = "http://nostalgic_mahavira:5000/upload"
DICOM_FOLDER = "/app/data/uploads"
DOWNLOAD_SUFFIX = "_downloaded.dcm"


def get_downloaded_dicom_files(folder: str) -> List[str]:
    return [f for f in os.listdir(folder) if f.endswith(DOWNLOAD_SUFFIX)]


def modify_dicom(dicom_path: str, output_folder: str) -> str:
    ds = pydicom.dcmread(dicom_path)
    ds.PatientName = getattr(ds, "PatientName", "Test Patient")
    ds.PatientID = getattr(ds, "PatientID", "123456")
    ds.StudyDescription = "Test Study"
    ds.SeriesDescription = "Processed Images"
    ds.StudyInstanceUID = pydicom.uid.generate_uid()
    ds.SeriesInstanceUID = pydicom.uid.generate_uid()

    modified_file_name = f"mod_{os.path.basename(dicom_path)}"
    modified_path = os.path.join(output_folder, modified_file_name)
    ds.save_as(modified_path)

    return modified_path


def upload_to_monai(file_path: str) -> bool:
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(MONAI_URL, files=files)

    if response.status_code == 200:
        print(f"✅ {os.path.basename(file_path)} subido con éxito a MONAI Deploy.")
        return True

    print(f"❌ Error al subir {os.path.basename(file_path)}: {response.status_code}, {response.text}")
    return False


def delete_file_if_exists(file_path: str, label: str):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"✅ {label} eliminado: {file_path}")
    else:
        print(f"❌ {label} no encontrado para eliminar: {file_path}")


class UploadToMONAIOperator(Operator):
    def init(self, fragment):
        super().init(fragment)

    def compute(self, context):
        dicom_files = get_downloaded_dicom_files(DICOM_FOLDER)

        if not dicom_files:
            print("❌ No hay archivos DICOM descargados con '_downloaded.dcm' en la carpeta.")
            return

        for filename in dicom_files:
            dicom_path = os.path.join(DICOM_FOLDER, filename)

            try:
                modified_path = modify_dicom(dicom_path, DICOM_FOLDER)

                if not os.path.exists(modified_path):
                    print(f"❌ El archivo modificado no existe: {modified_path}")
                    continue

                upload_to_monai(modified_path)
                delete_file_if_exists(dicom_path, "Archivo original")

            except Exception as e:
                print(f"❌ Error al procesar {dicom_path}: {e}")
