from orthanc.download_orthanc import DownloadFromOrthanc
from application.main_application import MainApplication
from orthanc.send_orthanc import SendToOrthancOperator

INFERRED_FOLDER = "/app/data/inferred"  

def run_pipeline():
    print("=== CICLO COMPLETO INICIADO ===")

    # Paso 1: Descargar DICOM desde Orthanc
    downloader = DownloadFromOrthanc()
    downloader.run()

    # Paso 2: Ejecutar MONAI para procesar la imagen
    monai_app = MainApplication()
    monai_app.run()

    # Paso 3: Subir imagen inferida de vuelta a Orthanc
    sender = SendToOrthancOperator(folder=INFERRED_FOLDER)
    sender.compute()

    print("✅ CICLO COMPLETO FINALIZADO")

if __name__ == "__main__":
    run_pipeline()

