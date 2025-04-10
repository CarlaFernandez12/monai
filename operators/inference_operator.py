import os
import torch
import pydicom
from monai.deploy.core import Operator, ExecutionContext, Fragment
from monai.transforms import LoadImage, EnsureChannelFirst, Resize, ScaleIntensity
from monai.networks.nets import UNet
from utils.dicom_utils import read_dicom, modify_metadata, save_modified_dicom  

DICOM_FOLDER = "/app/data/downloads"
MODEL_PATH = "/app/model.pt"
INFERRED_FOLDER = "/app/data/inferred"

class InferenceOperator(Operator):
    def __init__(self, fragment: Fragment): 
        super().__init__(fragment)

    def compute(self, context: ExecutionContext):
        print("🧠 Ejecutando inferencia...")

        if not os.path.exists(INFERRED_FOLDER):
            os.makedirs(INFERRED_FOLDER)

        image_files = [f for f in os.listdir(DICOM_FOLDER) if f.endswith("_downloaded.dcm")]
        if not image_files:
            print("❌ No hay imágenes para procesar.")
            return

        for img_file in image_files:
            img_path = os.path.join(DICOM_FOLDER, img_file)

            image = LoadImage()(img_path)
            image = EnsureChannelFirst()(image)
            image = ScaleIntensity()(image)
            image = Resize((128, 128, 128))(image)

            model = UNet(spatial_dims=3, in_channels=1, out_channels=1, channels=(16, 32, 64, 128), strides=(2, 2, 2), num_res_units=2)
            model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"), strict=False)

            model.eval()

            with torch.no_grad():
                output = model(image.unsqueeze(0))
                print("✅ Inferencia completada.")

                output_image = output.squeeze().cpu().numpy()

                dicom = read_dicom(img_path)
                dicom.PixelData = output_image.tobytes()

                if len(output_image.shape) == 3:
                    dicom.Rows, dicom.Columns, _ = output_image.shape
                else:
                    dicom.Rows, dicom.Columns = output_image.shape

                dicom = modify_metadata(dicom)

                result_dicom_path = save_modified_dicom(dicom, img_path, INFERRED_FOLDER)
                print(f"✅ Resultado guardado como DICOM en: {result_dicom_path}")

            print(f"Archivos en la carpeta de inferencia: {os.listdir(INFERRED_FOLDER)}")
