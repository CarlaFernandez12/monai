from pynetdicom import AE
from pynetdicom.sop_class import Verification
from config import ORTHANC_IP, ORTHANC_PORT, ORTHANC_AE_TITLE, CLIENT_AE_TITLE

def authenticate_with_orthanc():
    ae = AE(ae_title=CLIENT_AE_TITLE)
    ae.add_requested_context(Verification)

    print(f"🔄 Attempting to establish association with {ORTHANC_IP}:{ORTHANC_PORT} as AE Title '{ORTHANC_AE_TITLE}'...")

    assoc = ae.associate(addr=ORTHANC_IP, port=ORTHANC_PORT, ae_title=ORTHANC_AE_TITLE)

    if assoc.is_established:
        print("✅ DICOM association established successfully.")

        status = assoc.send_c_echo()

        if status and status.Status == 0x0000:
            print("✅ C-ECHO successful: Orthanc server responded correctly.")
        else:
            print(f"⚠️ C-ECHO failed. Status: {status}")

        assoc.release()
    else:
        print("❌ DICOM association with Orthanc could not be established.")

if __name__ == "__main__":
    authenticate_with_orthanc()
