from inference import InferenceOperator
from send_new_orthanc import send_to_orthanc_dicom

def main():
    print("🚀 Starting inference process...")
    operator = InferenceOperator()
    processed_files = operator.run()

    for dicom_path in processed_files:
        send_to_orthanc_dicom(dicom_path)

    print("✅ All files processed and sent to Orthanc.")

if __name__ == "__main__":
    main()

