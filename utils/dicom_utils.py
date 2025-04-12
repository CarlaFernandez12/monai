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

def save_modified_dicom(ds: pydicom.Dataset, original_path: str, output_folder: str) -> str:
    filename = os.path.basename(original_path)
    
    if not filename.startswith("mod_"):
        filename = f"mod_{filename}"
    
    output_path = os.path.join(output_folder, filename)
    
    ds.save_as(output_path)
    
    return output_path
 