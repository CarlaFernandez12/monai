import requests
from typing import Optional

ORTHANC_URL = "http://orthanc:8042"
AUTH = ("orthanc", "orthanc")

def upload_dicom_to_orthanc(file_path: str) -> bool:
    with open(file_path, "rb") as f:
        response = requests.post(
            f"{ORTHANC_URL}/instances",
            data=f,
            headers={"Content-Type": "application/dicom"},
            auth=AUTH,
        )
    return response.status_code in {200, 201, 202}

def get_all_instance_ids() -> list:
    response = requests.get(f"{ORTHANC_URL}/instances", auth=AUTH)
    return response.json() if response.status_code == 200 else []

def download_instance_file(instance_id: str) -> Optional[bytes]:
    response = requests.get(f"{ORTHANC_URL}/instances/{instance_id}/file", auth=AUTH)
    return response.content if response.status_code == 200 else None