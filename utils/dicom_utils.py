import os
import pydicom

def read_dicom(path: str) -> pydicom.Dataset:
    return pydicom.dcmread(path)

def modify_metadata(ds: pydicom.Dataset) -> pydicom.Dataset:
    ds.PatientName = "Test Patient"
    ds.PatientID = "123456"
    ds.StudyDescription = "Test Study"
    ds.SeriesDescription = "Processed Images"
    ds.StudyInstanceUID = pydicom.uid.generate_uid()
    ds.SeriesInstanceUID = pydicom.uid.generate_uid()
    return ds

def save_modified_dicom(dicom, original_path, output_dir):
    base_name = os.path.basename(original_path)
    save_path = os.path.join(output_dir, f"mod_{base_name}")

    dicom.ImageComments = f"Processed and saved at: {save_path}"

    dicom.save_as(save_path, write_like_original=False)
    return save_path

 