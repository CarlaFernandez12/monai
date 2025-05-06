from pynetdicom import AE, evt
from pynetdicom.sop_class import CTImageStorage, MRImageStorage
from pydicom.dataset import Dataset
import os

# Definir el directorio donde se guardarán las imágenes
storage_dir = '/app/DICOM/storage/'
os.makedirs(storage_dir, exist_ok=True)

# Definir un manejador para el evento C-STORE (cuando se recibe una imagen)
def handle_store(event):
    """Manejador para el evento C-STORE"""
    # Asegurarse de que el dataset contiene datos de píxeles
    if 'PixelData' in event.dataset:
        try:
            # Crear el nombre de archivo usando el SOPInstanceUID
            file_path = os.path.join(storage_dir, f"{event.dataset.SOPInstanceUID}.dcm")
            
            # Escribir la imagen DICOM en el archivo
            event.dataset.save_as(file_path, write_like_original=False)
            
            print(f"✅ Imagen guardada correctamente en {file_path}")
            return 0x0000  # Código de éxito en la respuesta C-STORE
        except Exception as e:
            print(f"⚠️ Error al guardar la imagen: {e}")
            return 0xA700  # Código de error en C-STORE
    else:
        print("⚠️ El DICOM recibido no contiene datos de píxeles.")
        return 0xA700  # Código de error en C-STORE

# Crear la aplicación AE (Application Entity)
ae = AE()

# Añadir los contextos de presentación para almacenamiento DICOM
ae.add_supported_context(CTImageStorage)
ae.add_supported_context(MRImageStorage)

# Establecer los manejadores de eventos
handlers = [(evt.EVT_C_STORE, handle_store)]

# Iniciar el servidor DICOM para escuchar en el puerto 11112
print(f"🟢 Esperando imágenes DICOM en el puerto 11112...")
ae.start_server(('', 11112), evt_handlers=handlers, block=True)
