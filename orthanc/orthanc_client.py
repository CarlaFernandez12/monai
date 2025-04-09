import os
import requests
import pydicom

ORTHANC_URL = "http://orthanc:8042"
AUTH = ("orthanc", "orthanc")
UPLOAD_FOLDER = "/app/data/uploads"
DOWNLOAD_FOLDER = "/app/data/uploads"  

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

class OrthancClient:
    def __init__(self):
        self.base_url = ORTHANC_URL
        self.auth = AUTH

    def upload_dicom(self, dicom_path):
        try:
            ds = pydicom.dcmread(dicom_path)
            ds.PatientName = "Test Patient"
            ds.PatientID = "123456"
            ds.StudyDescription = "Test Study"
            ds.SeriesDescription = "Processed Images"
            ds.StudyInstanceUID = pydicom.uid.generate_uid()
            ds.SeriesInstanceUID = pydicom.uid.generate_uid()

            modified_file_name = f"mod_{os.path.basename(dicom_path)}"
            modified_path = os.path.join(UPLOAD_FOLDER, modified_file_name)
            ds.save_as(modified_path)

            existing_files = requests.get(f"{self.base_url}/instances", auth=self.auth).json()
            if any(os.path.basename(modified_file_name) in file for file in existing_files):
                print(f"⚠ La imagen {modified_file_name} ya está en Orthanc.")
                return

            with open(modified_path, "rb") as dicom_file:
                response = requests.post(f"{self.base_url}/instances", data=dicom_file, 
                                         headers={"Content-Type": "application/dicom"}, auth=self.auth)

            if response.status_code in [200, 201, 202]:
                print(f"✅ Subido: {modified_file_name}")
            else:
                print(f"❌ Error en la subida: {response.status_code}")

        except Exception as e:
            print(f"❌ Error al subir {dicom_path}: {e}")

    def download_first_dicom(self):
        try:

            instances = requests.get(f"{self.base_url}/instances", auth=self.auth).json()
            if not instances:
                print("❌ No hay imágenes DICOM disponibles.")
                return

            instance_id = instances[0]
            file_response = requests.get(f"{self.base_url}/instances/{instance_id}/file", auth=self.auth)

            if file_response.status_code == 200:
                filename = f"{instance_id}_downloaded.dcm"
                output_path = os.path.join(DOWNLOAD_FOLDER, filename)

                if os.path.exists(output_path):
                    print(f"⚠ El archivo {filename} ya existe.")
                    return

                with open(output_path, "wb") as f:
                    f.write(file_response.content)
                print(f"✅ Descargada: {output_path}")

        except Exception as e:
            print(f"❌ Error inesperado al descargar:{e}")