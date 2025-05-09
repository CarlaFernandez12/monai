from pynetdicom import AE
from pynetdicom.sop_class import (
    StudyRootQueryRetrieveInformationModelFind,
    StudyRootQueryRetrieveInformationModelMove,
    CTImageStorage
)
from pydicom.dataset import Dataset
from config import ORTHANC_IP, ORTHANC_PORT, ORTHANC_AET

LOCAL_AET = 'MYCLIENT'
DEST_AET = 'MYLISTENER' 

def create_ae():
    ae = AE(ae_title=LOCAL_AET)
    ae.add_requested_context(StudyRootQueryRetrieveInformationModelFind)
    ae.add_requested_context(StudyRootQueryRetrieveInformationModelMove)
    ae.add_requested_context(CTImageStorage)
    return ae

def find_studies(ae):
    query = Dataset()
    query.QueryRetrieveLevel = 'STUDY'
    query.StudyDate = ''
    query.StudyInstanceUID = ''
    query.PatientID = ''
    query.PatientName = ''
    query.ModalitiesInStudy = ''

    assoc = ae.associate(ORTHANC_IP, ORTHANC_PORT, ae_title=ORTHANC_AET)
    if not assoc.is_established:
        print("❌ Failed to establish association with Orthanc (C-FIND)")
        return []

    print("✅ Association established with Orthanc (C-FIND)")
    study_uids = []

    for status, identifier in assoc.send_c_find(query, StudyRootQueryRetrieveInformationModelFind):
        if status and status.Status in (0xFF00, 0xFF01):  
            uid = getattr(identifier, 'StudyInstanceUID', None)
            if uid:
                study_uids.append(uid)
                print(f"➡️ Found StudyInstanceUID: {uid}")
        elif status and status.Status == 0x0000:
            print("✅ C-FIND completed")
        else:
            print(f"⚠️ C-FIND response status: 0x{status.Status:04x}")

    assoc.release()
    return study_uids

def move_study(ae, study_uid):
    move_ds = Dataset()
    move_ds.QueryRetrieveLevel = 'STUDY'
    move_ds.StudyInstanceUID = study_uid

    assoc = ae.associate(ORTHANC_IP, ORTHANC_PORT, ae_title=ORTHANC_AET)
    if not assoc.is_established:
        print("❌ Failed to establish association with Orthanc (C-MOVE)")
        return

    print(f"\n🚚 Sending C-MOVE request for StudyInstanceUID: {study_uid} to AE: {DEST_AET}")

    for status, identifier in assoc.send_c_move(move_ds, DEST_AET, StudyRootQueryRetrieveInformationModelMove):
        if status:
            print(f"🟢 C-MOVE status: 0x{status.Status:04x}")
        else:
            print("🔴 No response received")

    assoc.release()
    print("🔁 C-MOVE association released")

def main():
    ae = create_ae()
    studies = find_studies(ae)

    if not studies:
        print("❌ No studies found in Orthanc")
        return

    selected_uid = input("\n📝 Enter the StudyInstanceUID to move from Orthanc:\n> ").strip()

    if selected_uid not in studies:
        print("⚠️ The provided StudyInstanceUID is not in the retrieved list")
        return

    move_study(ae, selected_uid)

if __name__ == "__main__":
    main()
