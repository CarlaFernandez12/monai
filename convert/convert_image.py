import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

from convert.convert_to_dicom import convert_mhd_to_dicom

DATA_DIR = os.path.join(BASE_DIR, "data", "subset0")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "dicom")


def main():
    image_files = sorted([
        os.path.join(DATA_DIR, f)
        for f in os.listdir(DATA_DIR)
        if f.endswith('.mhd')
    ])

    if not image_files:
        print("No se encontraron imágenes en formato .mhd.")
        return

    print(f"Total de imágenes: {len(image_files)}")

    for mhd_file in image_files:
        print(f"Convirtiendo {mhd_file} a DICOM...")
        convert_mhd_to_dicom(mhd_file, OUTPUT_DIR)


if __name__ == '__main__':
    main()