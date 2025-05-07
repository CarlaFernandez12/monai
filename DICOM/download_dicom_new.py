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


assoc = ae.associate(ORTHANC_IP, ORTHANC_PORT, ae_title=ORTHANC_AET)

if assoc.is_established:
    print("✅ Association established with Orthanc for C-MOVE")


    responses = assoc.send_c_move(ds, MOVE_DEST_AET, StudyRootQueryRetrieveInformationModelMove)

    for (status, identifier) in responses:
        if status:
            try:
                print(f"🟢 C-MOVE Status: 0x{status.Status:04x}")
            except AttributeError:
                print("⚠️ Response status without 'Status' attribute")
        else:
            print("🔴 Error: No response received from the server")

    assoc.release()
    print("🔁 Association with Orthanc closed")
else:
    print("❌ Failed to establish association with Orthanc")
