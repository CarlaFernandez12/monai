import os
import pydicom
from pynetdicom import AE
from pynetdicom.sop_class import CTImageStorage, MRImageStorage, SecondaryCaptureImageStorage
import logging
logger = logging.getLogger()

ORTHANC_HOST = 'orthanc'     
ORTHANC_PORT = 4242
ORTHANC_AET = 'ORTHANC'
CLIENT_AET = 'CLIENT_AE'
DICOM_DIR = '/app/data/uploads' \
'' 

ae = AE(ae_title=CLIENT_AET)

ae.add_requested_context(CTImageStorage)
ae.add_requested_context(MRImageStorage)
ae.add_requested_context(SecondaryCaptureImageStorage)

assoc = ae.associate(ORTHANC_HOST, ORTHANC_PORT, ae_title=ORTHANC_AET)

if assoc.is_established:
    print("✅ Asociación establecida con Orthanc")

    for root, _, files in os.walk(DICOM_DIR):
        for filename in files:
            if filename.lower().endswith('.dcm'):
                filepath = os.path.join(root, filename)
                try:
                    ds = pydicom.dcmread(filepath)
                    if 'StudyInstanceUID' not in ds:
                        # Generar uno nuevo
                        ds.StudyInstanceUID = "KJABSDKJABSDK"
                        print(f"Se ha añadido StudyInstanceUID: {ds.StudyInstanceUID}")
                    status = assoc.send_c_store(ds)
                    print(ds)
                    if status and status.Status == 0x0000:
                        print(f"✅ Subido: {filename}")
                    else:
                        print(f"❌ Fallo al subir {filename}: {status}")
                except Exception as e:
                    print(f"⚠️ Error con {filename}: {e}")

    assoc.release()
    print("🔁 Asociación cerrada")
else:
    print("❌ No se pudo establecer conexión con Orthanc")
