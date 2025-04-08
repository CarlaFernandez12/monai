import os
import requests
import pydicom
from monai.deploy.core import Operator
from holoscan.core import Application, Fragment

ORTHANC_URL = "http://orthanc:8042/instances"
DICOM_FOLDER = "/app/data/uploads"
AUTH = ("orthanc", "orthanc")

class SendToOrthancOperator(Operator):
    def init(self, fragment):
        super().init(fragment)

    def compute(self, context):
        dicom_files = [f for f in os.listdir(DICOM_FOLDER) if f.endswith(".dcm")]
        
        if not dicom_files:
            print("❌ No hay archivos DICOM en la carpeta.")
            return

        for dicom_file in dicom_files:
            dicom_path = os.path.join(DICOM_FOLDER, dicom_file)
            print(f"📤 Subiendo {dicom_path} a Orthanc...")

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

                if not os.path.exists(modified_path):
                    print(f"❌ El archivo modificado no existe: {modified_path}")
                    continue
                else:
                    print(f"✅ Archivo modificado: {modified_path}")

                if os.path.exists(dicom_path):
                    os.remove(dicom_path)
                    print(f"🗑️ Eliminado original: {dicom_path}")

                try:
                    test_response = requests.get(ORTHANC_URL, auth=AUTH)
                    if test_response.status_code not in [200, 401]:
                        print(f"⚠️ Orthanc respondió pero no está aceptando conexiones: {test_response.status_code}")
                        continue
                except Exception as e:
                    print(f"❌ Orthanc no está accesible: {e}")
                    continue

                # Subida del DICOM
                with open(modified_path, "rb") as dicom_file:
                    upload_response = requests.post(
                        ORTHANC_URL,
                        data=dicom_file,
                        headers={"Content-Type": "application/dicom"},
                        auth=AUTH
                    )

                if upload_response.status_code in [200, 201, 202]:
                    print(f"✅ {modified_file_name} subido correctamente.")
                else:
                    print(f"❌ Falló la subida: {upload_response.status_code} → {upload_response.text}")

            except Exception as e:
                print(f"❌ Error al procesar {dicom_path}: {e}")

if __name__ == "__main__":
    app = Application()
    fragment = Fragment(app)
    operator = SendToOrthancOperator(fragment)
    operator.compute(None)
