from pynetdicom import AE, evt
from pynetdicom.sop_class import CTImageStorage, MRImageStorage
from pydicom.dataset import Dataset
import os

storage_dir = '/app/DICOM/storage/'
os.makedirs(storage_dir, exist_ok=True)

def handle_store(event):
    if 'PixelData' in event.dataset:
        try:
            file_path = os.path.join(storage_dir, f"{event.dataset.SOPInstanceUID}.dcm")

            event.dataset.save_as(file_path, write_like_original=False)
            
            print(f"✅ Image saved in {file_path}")
            return 0x0000  
        except Exception as e:
            print(f"⚠️ Error saving the image: {e}")
            return 0xA700  
    else:
        print("⚠️ The received DICOM does not contain pixel data.")
        return 0xA700  

ae = AE()

ae.add_supported_context(CTImageStorage)
ae.add_supported_context(MRImageStorage)


handlers = [(evt.EVT_C_STORE, handle_store)]

print(f"🟢 Waiting for DICOM images on port 11112...")
ae.start_server(('', 11112), evt_handlers=handlers, block=True)
