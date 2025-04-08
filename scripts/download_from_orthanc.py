import os
import requests

ORTHANC_URL = "http://orthanc:8042"

USERNAME = "orthanc"
PASSWORD = "orthanc"

DOWNLOAD_FOLDER = "/data/uploads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_first_dicom():
    try:
        instances_url = f"{ORTHANC_URL}/instances"
        print(f"Conectando a Orthanc en {instances_url}...")  
        response = requests.get(instances_url, auth=(USERNAME, PASSWORD))

        if response.status_code != 200:
            print(f"❌ No se pudieron obtener instancias: {response.status_code}")
            print(f"Detalles: {response.text}")  
            return

        instances = response.json()
        print(f"Instancias obtenidas: {instances}") 

        if not instances:
            print("❌ No hay imágenes DICOM en Orthanc.")
            return

        instance_id = instances[0]
        file_url = f"{ORTHANC_URL}/instances/{instance_id}/file"
        print(f"Descargando archivo desde {file_url}...")  
        file_response = requests.get(file_url, auth=(USERNAME, PASSWORD))

        if file_response.status_code == 200:
            output_path = os.path.join(DOWNLOAD_FOLDER, "original.dcm")
            with open(output_path, "wb") as f:
                f.write(file_response.content)
            print(f"✅ Imagen DICOM descargada correctamente a {output_path}")
        else:
            print(f"❌ Error al descargar la imagen: {file_response.status_code}")
            print(f"Detalles: {file_response.text}")  
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    download_first_dicom()
