from pynetdicom import AE, evt, AllStoragePresentationContexts
from pydicom import dcmread
import os
from config import LISTENING_PORT

SAVE_DIR = "/uploads/"

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def handle_store(event):
    ds = event.dataset
    ds.file_meta = event.file_meta

    sop_instance_uid = ds.SOPInstanceUID
    save_path = os.path.join(SAVE_DIR, f"{sop_instance_uid}.dcm")
    ds.save_as(save_path, write_like_original=False)
    print(f"[+] Image received and saved in: {save_path}")
    return 0x0000  

ae = AE()
ae.supported_contexts = AllStoragePresentationContexts

ae.ae_title = b"monai_s2" 

handlers = [(evt.EVT_C_STORE, handle_store)]

print("[*] Listening on LISTENING_PORT as C-STORE SCP server...")
ae.start_server(("", LISTENING_PORT), evt_handlers=handlers, block=True)
