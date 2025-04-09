import os
import requests
import pydicom
from typing import Optional

ORTHANC_URL = "http://orthanc:8042"
AUTH = ("orthanc", "orthanc")
UPLOAD_FOLDER = "/app/data/uploads"
DOWNLOAD_FOLDER = "/app/data/uploads"
VALID_UPLOAD_STATUS = {200, 201, 202}

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


def modify_dicom_metadata(ds: pydicom.Dataset) -> pydicom.Dataset:
    ds.PatientName = "Test Patient"
    ds.PatientID = "123456"
    ds.StudyDescription = "Test Study"
    ds.SeriesDescription = "Processed Images"
    ds.StudyInstanceUID = pydicom.uid.generate_uid()
    ds.SeriesInstanceUID = pydicom.uid.generate_uid()
    return ds


def save_dicom(ds: pydicom.Dataset, original_path: str) -> str:
    filename = f"mod_{os.path.basename(original_path)}"
    full_path = os.path.join(UPLOAD_FOLDER, filename)
    ds.save_as(full_path)
    return full_path


def already_uploaded(file_name: str) -> bool:
    try:
        instances = requests.get(f"{ORTHANC_URL}/instances", auth=AUTH).json()
        return any(file_name in entry for entry in instances)
    except Exception:
        return False


def upload_to_orthanc(dicom_path: str) -> bool:
    with open(dicom_path, "rb") as dicom_file:
        response = requests.post(
            f"{ORTHANC_URL}/instances",
            data=dicom_file,
            headers={"Content-Type": "application/dicom"},
            auth=AUTH,
        )
    return response.status_code in VALID_UPLOAD_STATUS


def download_first_instance_id() -> Optional[str]:
    try:
        instances = requests.get(f"{ORTHANC_URL}/instances", auth=AUTH).json()
        return instances[0] if instances else None
    except Exception:
        return None


def download_instance_file(instance_id: str) -> Optional[bytes]:
    response = requests.get(f"{ORTHANC_URL}/instances/{instance_id}/file", auth=AUTH)
    return response.content if response.status_code == 200 else None


def file_already_exists(filename: str) -> bool:
    return os.path.exists(os.path.join(DOWNLOAD_FOLDER, filename))


def save_file(content: bytes, filename: str):
    with open(os.path.join(DOWNLOAD_FOLDER, filename), "wb") as f:
        f.write(content)


class OrthancClient:
    def upload_dicom(self, dicom_path: str):
        try:
            ds = pydicom.dcmread(dicom_path)
            ds = modify_dicom_metadata(ds)
            modified_path = save_dicom(ds, dicom_path)
            filename = os.path.basename(modified_path)

            if already_uploaded(filename):
                print(f"⚠ La imagen {filename} ya está en Orthanc.")
                return

            if upload_to_orthanc(modified_path):
                print(f"✅ Subido: {filename}")
            else:
                print("❌ Error en la subida.")

        except Exception as e:
            print(f"❌ Error al subir {dicom_path}: {e}")

    def download_first_dicom(self):
        try:
            instance_id = download_first_instance_id()
            if not instance_id:
                print("❌ No hay imágenes DICOM disponibles.")
                return

            filename = f"{instance_id}_downloaded.dcm"
            if file_already_exists(filename):
                print(f"⚠ El archivo {filename} ya existe.")
                return

            content = download_instance_file(instance_id)
            if content:
                save_file(content, filename)
                print(f"✅ Descargada: {os.path.join(DOWNLOAD_FOLDER, filename)}")

        except Exception as e:
            print(f"❌ Error inesperado al descargar: {e}")
