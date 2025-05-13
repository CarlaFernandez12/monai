import os
import pydicom
import logging
from pynetdicom import AE
from pynetdicom.sop_class import (
    CTImageStorage,
    MRImageStorage,
    SecondaryCaptureImageStorage
)
from config import ORTHANC_HOST, ORTHANC_PORT, ORTHANC_AET, CLIENT_AE_TITLE, DICOM_DIR

logger = logging.getLogger()


def initialize_ae():
    ae = AE(ae_title=CLIENT_AE_TITLE)
    ae.add_requested_context(CTImageStorage)
    ae.add_requested_context(MRImageStorage)
    ae.add_requested_context(SecondaryCaptureImageStorage)
    return ae


def upload_dicom_file(filepath, assoc):
    try:
        ds = pydicom.dcmread(filepath)
        filename = os.path.basename(filepath)

        patient_id = getattr(ds, "PatientID", None)
        if not patient_id:
            logger.warning(f"⚠️ DICOM file {filename} has no PatientID. Uploading anyway.")
        else:
            logger.info(f"📌 Uploading file for PatientID: {patient_id}")

        status = assoc.send_c_store(ds)
        print(ds)
        if status and status.Status == 0x0000:
            print(f"✅ Uploaded: {filename}")
        else:
            print(f"❌ Failed to upload {filename}: {status}")
    except Exception as e:
        print(f"⚠️ Error with {filepath}: {e}")


def upload_all_dicoms(ae):
    assoc = ae.associate(ORTHANC_HOST, ORTHANC_PORT, ae_title=ORTHANC_AET)
    if not assoc.is_established:
        print("❌ Could not establish connection with Orthanc")
        return

    print("✅ Association established with Orthanc")

    for root, _, files in os.walk(DICOM_DIR):
        dicom_files = [f for f in files if f.lower().endswith('.dcm')]
        for filename in dicom_files:
            filepath = os.path.join(root, filename)
            upload_dicom_file(filepath, assoc)

    assoc.release()
    print("🔁 Association closed")


if __name__ == "__main__":
    ae = initialize_ae()
    upload_all_dicoms(ae)
