import os
import pydicom
from pynetdicom import AE
from pynetdicom.sop_class import CTImageStorage, MRImageStorage, SecondaryCaptureImageStorage
from config import ORTHANC_HOST, ORTHANC_PORT, ORTHANC_AET, CLIENT_AE_TITLE, DICOM_DIR
import logging
logger = logging.getLogger()

ae = AE(ae_title=CLIENT_AE_TITLE)

ae.add_requested_context(CTImageStorage)
ae.add_requested_context(MRImageStorage)
ae.add_requested_context(SecondaryCaptureImageStorage)

assoc = ae.associate(ORTHANC_HOST, ORTHANC_PORT, ae_title=ORTHANC_AET)

if assoc.is_established:
    print("✅ Association established with Orthanc")

    for root, _, files in os.walk(DICOM_DIR):
        for filename in files:
            if filename.lower().endswith('.dcm'):
                filepath = os.path.join(root, filename)
                try:
                    ds = pydicom.dcmread(filepath)

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
                    print(f"⚠️ Error with {filename}: {e}")

    assoc.release()
    print("🔁 Association closed")
else:
    print("❌ Could not establish connection with Orthanc")
