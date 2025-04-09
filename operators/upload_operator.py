import os
import requests
from monai.deploy.core import Operator
from utils.dicom_utils import read_dicom, modify_metadata, save_modified_dicom
from utils.file_utils import list_files_with_suffix, remove_file

MONAI_URL = "http://nostalgic_mahavira:5000/upload"
DICOM_FOLDER = "/app/data/downloads"
DOWNLOAD_SUFFIX = "_downloaded.dcm"


def upload_to_monai(file_path: str) -> bool:
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(MONAI_URL, files=files)

    if response.status_code == 200:
        print(f"✅ {os.path.basename(file_path)} subido con éxito a MONAI Deploy.")
        return True

    print(f"❌ Error al subir {os.path.basename(file_path)}: {response.status_code}, {response.text}")
    return False


class UploadToMONAIOperator(Operator):
    def init(self, fragment):
        super().init(fragment)

    def compute(self, context):
        dicom_files = list_files_with_suffix(DICOM_FOLDER, DOWNLOAD_SUFFIX)

        if not dicom_files:
            print("❌ No hay archivos DICOM descargados con '_downloaded.dcm' en la carpeta.")
            return

        for filename in dicom_files:
            dicom_path = os.path.join(DICOM_FOLDER, filename)

            try:

                ds = read_dicom(dicom_path)
                modified_ds = modify_metadata(ds)
                modified_path = save_modified_dicom(modified_ds, dicom_path, DICOM_FOLDER)


                if not os.path.exists(modified_path):
                    print(f"❌ El archivo modificado no existe: {modified_path}")
                    continue

                upload_to_monai(modified_path)
                remove_file(dicom_path)

            except Exception as e:
                print(f"❌ Error al procesar {dicom_path}:{e}")