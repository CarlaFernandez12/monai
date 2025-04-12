import os
from typing import List

def list_dicom_files(folder: str) -> List[str]:
    return [f for f in os.listdir(folder) if f.endswith(".dcm")]

def list_files_with_suffix(folder: str, suffix: str) -> List[str]:
    return [f for f in os.listdir(folder) if f.endswith(suffix)]

def file_exists(path: str) -> bool:
    return os.path.exists(path)

def save_bytes(content: bytes, output_path: str):
    with open(output_path, "wb") as f:
        f.write(content)

def remove_file(path: str):
    if os.path.exists(path):
        os.remove(path)
 