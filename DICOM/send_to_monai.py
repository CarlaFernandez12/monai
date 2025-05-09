from pynetdicom import AE
from pynetdicom.sop_class import CTImageStorage
import pydicom

ae = AE(ae_title=b"client")  
ae.add_requested_context(CTImageStorage)

assoc = ae.associate("localhost", 11113, ae_title=b"monai_s2") 

if assoc.is_established:
    dicom_file = "/app/DICOM/storage/1.2.826.0.1.3680043.8.498.41178521339771585380306575116212618699.dcm"
    ds = pydicom.dcmread(dicom_file)

    status = assoc.send_c_store(ds)
    print(f"Status: 0x{status.Status:04x}")
    assoc.release()
else:
    print("Association failed")
