import subprocess
import os

def download_images():
    """Descargar imágenes desde Orthanc."""
    print("🔽 Iniciando descarga de imágenes desde Orthanc...")
    subprocess.run(["python", "/app/DICOM/download_dicom_new.py"])  # Ruta completa
    print("✅ Descarga completada.")

def upload_to_monai():
    """Subir imágenes a MONAI."""
    print("⬆️ Subiendo imágenes a MONAI...")
    subprocess.run(["python", "/app/DICOM/upload_monai.py"])  # Ruta completa
    print("✅ Imágenes subidas a MONAI.")

def inference():
    """Ejecutar inferencia en las imágenes."""
    print("🧠 Realizando inferencia en las imágenes...")
    subprocess.run(["python", "/app/DICOM/inference.py"])  # Ruta completa
    print("✅ Inferencia completada.")

def upload_processed_to_orthanc():
    """Subir las imágenes procesadas de vuelta a Orthanc."""
    print("⬆️ Subiendo imágenes procesadas a Orthanc...")
    subprocess.run(["python", "/app/DICOM/upload_dicom.py"])  # Ruta completa
    print("✅ Imágenes procesadas subidas a Orthanc.")


def run_full_flow():
    """Ejecutar todo el flujo de trabajo completo."""
    download_images()
    upload_to_monai()
    inference()
    upload_processed_to_orthanc()

if __name__ == "__main__":
    run_full_flow()
