# send_new_orthanc.py
import pydicom
from pynetdicom import AE
from pynetdicom.sop_class import CTImageStorage
from config import ORTHANC_HOST, ORTHANC_PORT, ORTHANC_AET

def send_to_orthanc_dicom(dicom_path, orthanc_host=ORTHANC_HOST, orthanc_port=ORTHANC_PORT, orthanc_aet=ORTHANC_AET):
    ae = AE(ae_title="MONAI")
    ae.add_requested_context(CTImageStorage)

    assoc = ae.associate(orthanc_host, orthanc_port, ae_title=orthanc_aet)

    if assoc.is_established:
        ds = pydicom.dcmread(dicom_path)
        status = assoc.send_c_store(ds)
        assoc.release()
        if status:
            print(f"✅ Sent {dicom_path} to Orthanc. Status: 0x{status.Status:04X}")
        else:
            print(f"❌ Failed to send {dicom_path}. No status returned.")
    else:
        print("❌ Could not connect to Orthanc.")
