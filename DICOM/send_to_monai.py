from pynetdicom import AE
from pynetdicom.sop_class import CTImageStorage
import pydicom
import os
from config import STORAGE_DIR, LISTENING_PORT

dicom_files = [f for f in os.listdir(STORAGE_DIR) if f.endswith(".dcm")]

if not dicom_files:
    print("No DICOM files found in the directory.")
    exit()

print("Available DICOM files:")
for i, file in enumerate(dicom_files):
    print(f"[{i}] {file}")

while True:
    try:
        choice = int(input("\nSelect the number of the file to upload: "))
        if 0 <= choice < len(dicom_files):
            break
        else:
            print("Number out of range.")
    except ValueError:
        print("Please enter a valid number.")

selected_file = os.path.join(STORAGE_DIR, dicom_files[choice])

ae = AE(ae_title=b"client")
ae.add_requested_context(CTImageStorage)

assoc = ae.associate("localhost", LISTENING_PORT, ae_title=b"monai_s2")

if assoc.is_established:
    ds = pydicom.dcmread(selected_file)
    status = assoc.send_c_store(ds)
    print(f"\nFile sent: {dicom_files[choice]}")
    print(f"Status: 0x{status.Status:04x}")
    assoc.release()
else:
    print("Association with DICOM server failed.")
