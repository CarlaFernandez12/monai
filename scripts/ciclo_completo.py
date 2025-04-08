import os
import requests
import torch
import pydicom
import numpy as np
from torch.optim import Adam
from torch.nn import MSELoss
from monai.deploy.core import Operator, Fragment, Application
from monai.transforms import (
    Compose, ScaleIntensityd, Resized,
    RandRotated, RandFlipd, RandZoomd
)
from monai.networks.nets import UNet
from monai.data import Dataset, DataLoader

# Configuración
ORTHANC_URL = "http://orthanc:8042"
MONAI_UPLOAD_URL = "http://localhost:5000/upload"
MONAI_DOWNLOAD_URL = "http://localhost:5000/download"
PROCESSED_FILENAME = "processed.dcm"
DOWNLOAD_FOLDER = "/data/uploads"
MODEL_PATH = "/model.pt"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def create_transform():
    return Compose([
        ScaleIntensityd(keys="image"),
        Resized(keys = "image", spatial_size=(128, 128)),
        RandRotated(keys = "image", range_x=np.pi / 12, prob=0.5, keep_size=True),
        RandFlipd(keys = "image", spatial_axis=0, prob=0.5),
        RandZoomd(keys = "image", min_zoom=0.9, max_zoom=1.1, prob=0.5),
    ])

def save_dicom_image(np_image, original_dicom, output_path):
    np_image = (np_image * 255).astype(np.uint8)
    original_dicom.PixelData = np_image.tobytes()
    original_dicom.Rows, original_dicom.Columns = np_image.shape
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    original_dicom.save_as(output_path)

class DownloadFromOrthancOperator(Operator):
    def __init__(self, fragment):
        super().__init__(fragment)
        self.dicom_path = os.path.join(DOWNLOAD_FOLDER, "input.dcm")

    def compute(self, context):
        print("Descargando imagen desde Orthanc...")
        r = requests.get(f"{ORTHANC_URL}/instances", auth=("orthanc", "orthanc"))
        instances = r.json()
        if not instances:
            raise RuntimeError("No se encontraron instancias en Orthanc.")
        instance_id = instances[0]
        file_url = f"{ORTHANC_URL}/instances/{instance_id}/file"
        r = requests.get(file_url, auth=("orthanc", "orthanc"))
        with open(self.dicom_path, "wb") as f:
            f.write(r.content)
        print(f"✅ Imagen DICOM descargada: {self.dicom_path}")
        return self.dicom_path

class UploadToMonaiOperator(Operator):
    def compute(self, context):
        path = os.path.join(DOWNLOAD_FOLDER, "input.dcm")
        if not os.path.exists(path):
            print("❌ No se encuentra la imagen DICOM para subir a MONAI.")
            return
        with open(path, "rb") as f:
            r = requests.post(MONAI_UPLOAD_URL, files={"file": f})
            print(f"📤 Subida a MONAI: {r.status_code} - {r.text}")

class ProcessImageWithModelOperator(Operator):
    def __init__(self, fragment):
        super().__init__(fragment)
        self.model = UNet(
            spatial_dims=2,
            in_channels=1,
            out_channels=1,
            channels=(16, 32, 64, 128),
            strides=(2, 2, 2),
            num_res_units=2,
        )
        self.transform = create_transform()

    def compute(self, context):
        dicom_path = os.path.join(DOWNLOAD_FOLDER, "input.dcm")
        self.model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"), strict=False)
        self.model.eval()

        ds = pydicom.dcmread(dicom_path)
        image = ds.pixel_array.astype(np.float32)
        image = np.expand_dims(image, axis=0)
        image = self.transform({"image": image})["image"]

        with torch.no_grad():
            output = self.model(image.unsqueeze(0))
        output = output.squeeze().numpy()
        output = (output - output.min()) / (output.max() - output.min() + 1e-5)

        output_path = os.path.join(DOWNLOAD_FOLDER, PROCESSED_FILENAME)
        save_dicom_image(output, ds, output_path)

        print(f"✅ Imagen procesada guardada: {output_path}")
        return output_path

class UploadProcessedToOrthancOperator(Operator):
    def compute(self, context):
        path = os.path.join(DOWNLOAD_FOLDER, PROCESSED_FILENAME)
        if not os.path.exists(path):
            print("❌ No se encuentra la imagen procesada.")
            return
        with open(path, "rb") as f:
            r = requests.post(
                f"{ORTHANC_URL}/instances", data=f,
                headers={"Content-Type": "application/dicom"},
                auth=("orthanc", "orthanc")
            )
            print(f"📤 Subida a Orthanc: {r.status_code} - {r.text}")

app = Application()

# Paso 1: Descargar imagen desde Orthanc
download_op = DownloadFromOrthancOperator(Fragment(app))
dicom_path = download_op.compute(None)

# Paso 2: Subir imagen a MONAI para procesamiento
upload_monai_op = UploadToMonaiOperator(Fragment(app))
upload_monai_op.compute(None)

# Paso 3: Procesar imagen con el modelo UNet
process_op = ProcessImageWithModelOperator(Fragment(app))
processed_path = process_op.compute(None)

# Paso 4: Subir la imagen procesada a Orthanc
upload_orthanc_op = UploadProcessedToOrthancOperator(Fragment(app))
upload_orthanc_op.compute(None)
