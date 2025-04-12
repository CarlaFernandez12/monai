from orthanc.download_orthanc import DownloadFromOrthanc
from application.main_application import MainApplication
from orthanc.send_orthanc import SendToOrthancOperator

INFERRED_FOLDER = "/app/data/inferred"  

def run_pipeline():
    print("=== FULL CYCLE STARTED ===")

    # Step 1: Download DICOM from Orthanc
    downloader = DownloadFromOrthanc()
    downloader.run()

    # Step 2: Run MONAI to process the image
    monai_app = MainApplication()
    monai_app.run()

    # Step 3: Upload inference image back to Orthanc
    sender = SendToOrthancOperator(folder=INFERRED_FOLDER)
    sender.compute()

    print("✅ FULL CYCLE COMPLETED")

if __name__ == "__main__":
    run_pipeline()

