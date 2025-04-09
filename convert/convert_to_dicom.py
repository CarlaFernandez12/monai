import os
import datetime
import numpy as np
import SimpleITK as sitk
import pydicom
from pydicom.dataset import Dataset, FileMetaDataset
from pydicom.uid import (
    ImplicitVRLittleEndian,
    CTImageStorage,
    generate_uid,
    PYDICOM_IMPLEMENTATION_UID
)


def convert_mhd_to_dicom(mhd_file, output_dir):
    image = sitk.ReadImage(mhd_file)
    image_array = sitk.GetArrayFromImage(image)

    file_meta = FileMetaDataset()
    file_meta.TransferSyntaxUID = ImplicitVRLittleEndian
    file_meta.MediaStorageSOPClassUID = CTImageStorage
    file_meta.MediaStorageSOPInstanceUID = generate_uid()
    file_meta.ImplementationClassUID = PYDICOM_IMPLEMENTATION_UID

    os.makedirs(output_dir, exist_ok=True)

    for i, slice_array in enumerate(image_array):
        dicom_file = Dataset()
        dicom_file.file_meta = file_meta

        dicom_file.PatientName = "LUNA16_Paciente"
        dicom_file.PatientID = "123456"
        dicom_file.StudyDate = datetime.datetime.now().strftime("%Y%m%d")
        dicom_file.Modality = "CT"
        dicom_file.SeriesInstanceUID = generate_uid()
        dicom_file.SOPInstanceUID = generate_uid()
        dicom_file.InstanceNumber = i + 1

        dicom_file.Rows, dicom_file.Columns = slice_array.shape
        dicom_file.PhotometricInterpretation = "MONOCHROME2"
        dicom_file.SamplesPerPixel = 1
        dicom_file.BitsAllocated = 16
        dicom_file.BitsStored = 16
        dicom_file.HighBit = 15
        dicom_file.PixelRepresentation = 1
        dicom_file.PixelData = slice_array.tobytes()

        output_path = os.path.join(output_dir, f"slice_{i+1:04d}.dcm")

        if os.path.exists(output_path):
            os.remove(output_path)
            
        pydicom.dcmwrite(output_path, dicom_file, write_like_original=False)

    print(f"Conversión de {mhd_file} a DICOM completada. Archivos guardados en {output_dir}")