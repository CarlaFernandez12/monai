import os

from utils.dicom_utils import read_dicom, modify_metadata, save_modified_dicom
from utils.file_utils import file_exists, save_bytes
from services.orthanc_service import (
    upload_dicom_to_orthanc,
    get_all_instance_ids,
    download_instance_file,
)

UPLOAD_FOLDER = "/app/data/uploads"
DOWNLOAD_FOLDER = "/app/data/downloads"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


class OrthancClient:
    def upload_dicom(self, dicom_path: str):
        try:
            ds = read_dicom(dicom_path)
            ds = modify_metadata(ds)
            modified_path = save_modified_dicom(ds, dicom_path, UPLOAD_FOLDER)
            filename = os.path.basename(modified_path)

            instance_ids = get_all_instance_ids()
            if any(filename in id_ for id_ in instance_ids):
                print(f"⚠ The image {filename} is already in Orthanc.")
                return

            if upload_dicom_to_orthanc(modified_path):
                print(f"✅ Uploaded: {filename}")
            else:
                print("❌ Error uploading.")

        except Exception as e:
            print(f"❌ Error uploading {dicom_path}: {e}")

    def download_first_dicom(self):
        try:
            instance_ids = get_all_instance_ids()
            if not instance_ids:
                print("❌ There are no DICOM images available.")
                return

            instance_id = instance_ids[0]
            filename = f"{instance_id}_downloaded.dcm"
            full_path = os.path.join(DOWNLOAD_FOLDER, filename)

            if file_exists(full_path):
                print(f"⚠ File {filename} already exists.")
                return

            content = download_instance_file(instance_id)
            if content:
                save_bytes(content, full_path)
                print(f"✅ Downloaded: {full_path}")
        except Exception as e:
            print(f"❌ Unexpected error while downloading:{e}")