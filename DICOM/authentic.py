from pynetdicom import AE
from pynetdicom.sop_class import Verification

CLIENT_AE_TITLE = "CLIENT_AE"
CLIENT_PORT = 11112  

ORTHANC_AE_TITLE = "ORTHANC"
ORTHANC_IP = "orthanc"  
ORTHANC_PORT = 4242

def authenticate_with_orthanc():
    """Establece una asociación DICOM con Orthanc y realiza un C-ECHO."""
    ae = AE(ae_title=CLIENT_AE_TITLE)
    ae.add_requested_context(Verification)

    print(f"🔄 Intentando establecer asociación con {ORTHANC_IP}:{ORTHANC_PORT} como AE Title '{ORTHANC_AE_TITLE}'...")

    assoc = ae.associate(addr=ORTHANC_IP, port=ORTHANC_PORT, ae_title=ORTHANC_AE_TITLE)

    if assoc.is_established:
        print("✅ Asociación DICOM establecida correctamente.")

        status = assoc.send_c_echo()

        if status and status.Status == 0x0000:
            print("✅ C-ECHO exitoso: el servidor Orthanc respondió correctamente.")
        else:
            print(f"⚠️ C-ECHO fallido. Status: {status}")

        assoc.release()
    else:
        print("❌ No se pudo establecer la asociación DICOM con Orthanc.")

if __name__ == "__main__":
    authenticate_with_orthanc()
