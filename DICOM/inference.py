import os
import torch
from monai.transforms import LoadImage, EnsureChannelFirst, Resize, ScaleIntensity
from monai.networks.nets import UNet
from utils.dicom_utils import read_dicom, modify_metadata, save_modified_dicom

MONAI_UPLOADS_DIR = "/uploads/"
MONAI_INFERRED_DIR = "/inferred/"
MODEL_PATH = "/app/model.pt"

class InferenceOperator:
    def __init__(self): 
        self.model = self._load_model()
        os.makedirs(MONAI_INFERRED_DIR, exist_ok=True)

    def _load_model(self):
        model = UNet(
            spatial_dims=3,
            in_channels=1,
            out_channels=1,
            channels=(16, 32, 64, 128),
            strides=(2, 2, 2),
            num_res_units=2
        )
        model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"), strict=False)
        model.eval()
        return model

    def run(self):
        image_files = [f for f in os.listdir(MONAI_UPLOADS_DIR) if f.endswith('.dcm')]
        if not image_files:
            print("❌ No DICOM images to process.")
            return []

        output_files = []

        for img_file in image_files:
            img_path = os.path.join(MONAI_UPLOADS_DIR, img_file)
            print(f"📥 Processing {img_path}...")

            image = LoadImage()(img_path)
            image = EnsureChannelFirst()(image)
            image = ScaleIntensity()(image)
            image = Resize((128, 128, 128))(image)

            with torch.no_grad():
                output = self.model(image.unsqueeze(0))
                output_image = output.squeeze().cpu().numpy()

            dicom = read_dicom(img_path)
            dicom.PixelData = output_image.tobytes()
            dicom = modify_metadata(dicom)

            if len(output_image.shape) == 3:
                dicom.Rows, dicom.Columns, _ = output_image.shape
            else:
                dicom.Rows, dicom.Columns = output_image.shape

            result_path = save_modified_dicom(dicom, img_path, MONAI_INFERRED_DIR)
            print(f"✅ Saved processed DICOM to: {result_path}")
            output_files.append(result_path)

        return output_files
