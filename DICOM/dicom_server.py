from pynetdicom import AE, evt
from pynetdicom.sop_class import CTImageStorage, MRImageStorage, UltrasoundImageStorage, SecondaryCaptureImageStorage, RTImageStorage, GrayscaleSoftcopyPresentationStateStorage
import logging

def handle_store(event):
    ds = event.dataset
    ds.file_meta = event.file_meta
    filename = f"/app/DICOM/received/{ds.SOPInstanceUID}.dcm"
    ds.save_as(filename, write_like_original=False)
    print(f"✅ Guardado: {filename}")
    return 0x0000

def start_dicom_server():
    ae = AE(ae_title="MONAI")
    
    # Añadir algunos contextos comunes de presentación para imágenes DICOM
    ae.add_supported_context(CTImageStorage)
    ae.add_supported_context(MRImageStorage)
    ae.add_supported_context(UltrasoundImageStorage)
    ae.add_supported_context(SecondaryCaptureImageStorage)
    ae.add_supported_context(RTImageStorage)
    ae.add_supported_context(GrayscaleSoftcopyPresentationStateStorage)

    handlers = [(evt.EVT_C_STORE, handle_store)]
    print("🩻 Servidor DICOM escuchando en puerto 11112...")
    ae.start_server(("0.0.0.0", 11112), evt_handlers=handlers, block=True)

if __name__ == "__main__":
    start_dicom_server()
