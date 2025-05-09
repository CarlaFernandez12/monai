from pynetdicom import AE, evt
from pynetdicom.sop_class import CTImageStorage, MRImageStorage
from pydicom.dataset import Dataset
import os
from config import STORAGE_DIR

os.makedirs(STORAGE_DIR, exist_ok=True)


class DICOMSaveError(Exception):
    """Raised when a DICOM file cannot be saved properly."""
    pass

class NoPixelDataError(Exception):
    """Raised when the DICOM file does not contain pixel data."""
    pass

def handle_store(event):
    try:
        if 'PixelData' not in event.dataset:
            raise NoPixelDataError("DICOM file has no PixelData.")

        sop_instance_uid = event.dataset.SOPInstanceUID
        file_path = os.path.join(STORAGE_DIR, f"{sop_instance_uid}.dcm")

        event.dataset.save_as(file_path, write_like_original=False)
        print(f"✅ DICOM file saved at: {file_path}")
        return 0x0000  

    except NoPixelDataError as e:
        print(f"⚠️ {e}")
        return 0xA700  

    except Exception as e:
        print(f"❌ Unexpected error during storage: {e}")
        return 0xA700 
    
ae = AE()

ae.add_supported_context(CTImageStorage)
ae.add_supported_context(MRImageStorage)


handlers = [(evt.EVT_C_STORE, handle_store)]

print("🟢 Listening for incoming DICOM files on port 11112...")
ae.start_server(('', 11112), evt_handlers=handlers, block=True)
