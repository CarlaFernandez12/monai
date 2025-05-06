import os
import torch
import pydicom
from monai.deploy.core import Operator, ExecutionContext, Fragment
from monai.transforms import LoadImage, EnsureChannelFirst, Resize, ScaleIntensity
from monai.networks.nets import UNet
from utils.dicom_utils import read_dicom, modify_metadata, save_modified_dicom
from pynetdicom import AE
from pynetdicom.sop_class import CTImageStorage

DICOM_FOLDER = "/app/data/downloads"
MODEL_PATH = "/app/model.pt"
INFERRED_FOLDER = "/app/data/inferred"

def send_to_orthanc_dicom(dicom_path, orthanc_host="orthanc", orthanc_port=4242, orthanc_aet="ORTHANC"):
    ae = AE(ae_title="MONAI")
    ae.add_requested_context(CTImageStorage)

    assoc = ae.associate(orthanc_host, orthanc_port, ae_title=orthanc_aet)

    if assoc.is_established:
        ds = pydicom.dcmread(dicom_path)
        status = assoc.send_c_store(ds)
        assoc.release()
        if status:
            print(f"✅ Sent {dicom_path} to Orthanc via DICOM. Status: 0x{status.Status:04X}")
        else:
            print(f"❌ Failed to send {dicom_path}. No status returned.")
    else:
        print("❌ Association with Orthanc failed.")


class InferenceOperator(Operator):
    def __init__(self, fragment: Fragment): 
        super().__init__(fragment)

    def compute(self, context: ExecutionContext):
        print("🧠 Running inference...")

        if not os.path.exists(INFERRED_FOLDER):
            os.makedirs(INFERRED_FOLDER)

        image_files = [f for f in os.listdir(DICOM_FOLDER) if f.endswith("_downloaded.dcm")]
        if not image_files:
            print("❌ There are no images to process.")
            return

        for img_file in image_files:
            img_path = os.path.join(DICOM_FOLDER, img_file)

            image = LoadImage()(img_path)
            image = EnsureChannelFirst()(image)
            image = ScaleIntensity()(image)
            image = Resize((128, 128, 128))(image)

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

            with torch.no_grad():
                output = model(image.unsqueeze(0))
                print("✅ Inference completed.")

                output_image = output.squeeze().cpu().numpy()

                dicom = read_dicom(img_path)
                dicom.PixelData = output_image.tobytes()

                if len(output_image.shape) == 3:
                    dicom.Rows, dicom.Columns, _ = output_image.shape
                else:
                    dicom.Rows, dicom.Columns = output_image.shape

                dicom = modify_metadata(dicom)
                result_dicom_path = save_modified_dicom(dicom, img_path, INFERRED_FOLDER)

                print(f"✅ Result saved as DICOM in: {result_dicom_path}")

                # Subir a Orthanc usando protocolo DICOM
                send_to_orthanc_dicom(result_dicom_path)

        print(f"📂 Files in the inference folder: {os.listdir(INFERRED_FOLDER)}")
