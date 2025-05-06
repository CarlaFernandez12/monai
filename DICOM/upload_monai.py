import os
import pydicom
from pydicom.uid import UID
from pynetdicom import AE, StoragePresentationContexts

# Parámetros
source_dicom_file = "/app/DICOM/storage/1.2.826.0.1.3680043.8.498.41178521339771585380306575116212618699.dcm"  # Archivo descargado desde Orthanc
target_ae_title = "MONAI"  # AE title de tu servidor MONAI
target_ip = "172.17.0.3"  # La IP de tu servidor MONAI
target_port = 5000  # El puerto en el que el servidor MONAI escucha (esto puede variar)

# Leer el archivo DICOM
ds = pydicom.dcmread(source_dicom_file)

# Iniciar la Asociación con MONAI
ae = AE()

# Añadir los contextos de presentación válidos para el almacenamiento (Storage)
for context in StoragePresentationContexts:
    ae.add_requested_context(context.abstract_syntax)

# Conectar con el servidor MONAI
assoc = ae.associate(target_ip, target_port, ae_title=target_ae_title)

if assoc.is_established:
    # Enviar la imagen DICOM a MONAI
    print(f"Enviando {source_dicom_file} a MONAI...")
    status = assoc.send_c_store(ds)

    if status:
        print(f"Envio exitoso. Status: {status}")
    else:
        print("Error al enviar la imagen a MONAI.")
    
    # Cerrar la asociación
    assoc.release()
else:
    print("No se pudo establecer la asociación con MONAI.")
