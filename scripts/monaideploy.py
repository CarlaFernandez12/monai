import os
import requests
import pydicom
from monai.deploy.core import Operator
from monai.deploy.core import Application
from monai.deploy.core import Fragment

MONAI_URL = "http://nostalgic_mahavira:5000/upload"  
DICOM_FOLDER = "/app/data/uploads"  

class UploadToMONAIOperator(Operator):
    def _init_(self, fragment):
        super()._init_(fragment)

    def compute(self, context):
        dicom_files = [f for f in os.listdir(DICOM_FOLDER) if f.endswith(".dcm")]
        
        if not dicom_files:
            print("❌ No hay archivos DICOM en la carpeta.")
            return

        for dicom_file in dicom_files:
            dicom_path = os.path.join(DICOM_FOLDER, dicom_file)
            print(f"📤 Subiendo {dicom_path} a MONAI Deploy...")

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
                    print(f"✅ El archivo modificado existe: {modified_path}")

                original_path = os.path.join(DICOM_FOLDER, dicom_file)
                if os.path.exists(original_path):
                    os.remove(original_path)  
                    print(f"✅ Archivo original eliminado: {original_path}")
                else:
                    print(f"❌ No se encontró el archivo original para eliminar: {original_path}")

                with open(modified_path, "rb") as dicom_file:
                     files = {"file": dicom_file}  
                     upload_response = requests.post(MONAI_URL,files=files)
                        

                if upload_response.status_code == 200:
                    print(f"✅ {modified_file_name} subido con éxito a MONAI Deploy.")
                else:
                    print(f"❌ Error al subir {modified_file_name}: {upload_response.status_code}, {upload_response.text}")

            except Exception as e:
                print(f"❌ Error al procesar {dicom_path}: {e}")

app = Application()
fragment = Fragment(app)

operator = UploadToMONAIOperator(fragment)
operator.compute(None)