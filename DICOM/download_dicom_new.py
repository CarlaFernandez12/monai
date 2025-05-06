from pynetdicom import AE
from pynetdicom.sop_class import StudyRootQueryRetrieveInformationModelMove, CTImageStorage
from pydicom.dataset import Dataset

ORTHANC_IP = 'orthanc' 
ORTHANC_PORT = 4242
ORTHANC_AET = 'ORTHANC'
MOVE_DEST_AET = 'MYLISTENER' 


STUDY_INSTANCE_UID = '1.2.826.0.1.3680043.8.498.28886909095893880233821241097520922568'


ae = AE(ae_title='MYCLIENT')  


ae.add_requested_context(StudyRootQueryRetrieveInformationModelMove)
ae.add_requested_context(CTImageStorage)


ds = Dataset()
ds.QueryRetrieveLevel = 'STUDY'
ds.StudyInstanceUID = STUDY_INSTANCE_UID

# Asociación
assoc = ae.associate(ORTHANC_IP, ORTHANC_PORT, ae_title=ORTHANC_AET)

if assoc.is_established:
    print("✅ Asociación establecida con Orthanc para C-MOVE")


    responses = assoc.send_c_move(ds, MOVE_DEST_AET, StudyRootQueryRetrieveInformationModelMove)

    for (status, identifier) in responses:
        if status:
            try:
                print(f"🟢 C-MOVE Status: 0x{status.Status:04x}")
            except AttributeError:
                print("⚠️ Estado de respuesta sin atributo 'Status'")
        else:
            print("🔴 Error: No se recibió respuesta del servidor")

    # Cerrar asociación
    assoc.release()
    print("🔁 Asociación con Orthanc cerrada")
else:
    print("❌ No se pudo establecer asociación con Orthanc")
