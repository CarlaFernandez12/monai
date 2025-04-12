
# 🫁 Lung Nodule Detection with MONAI Deploy

This project implements a full pipeline for working with medical images in DICOM format, using **MONAI Deploy** and a pretrained model for lung nodule detection on CT scans.

---

## 📦 Project Setup

To use this repository, you need to set up a Python virtual environment with MONAI and all required libraries.

### 1. Activate the MONAI Environment

Before running the pipeline, make sure that you have **Python 3.10** or higher installed. You can check your Python version by running the following command:

```bash
python --version
```

If you have the correct Python version, proceed with activating the environment.

In your terminal:

```bash
.\your_folder_name\Scripts\python.exe
```

Then activate the environment:

- On **Command Prompt or PowerShell**:

```bash
.\your_folder_name\Scriptsctivate
```

- On **Git Bash**:

```bash
source your_folder_name/Scripts/activate
```

### 2. Install Dependencies

Make sure you're inside the activated environment. Then run:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file should be located at the root of your project.

---

## 🗃 Dataset: LUNA16

This project uses the **LUNA16** dataset for lung CT scans. You must download it to access `.mhd` image files and convert them to DICOM for further processing.

🔗 **Download link**:  
[https://zenodo.org/records/3723295](https://zenodo.org/records/3723295)

After downloading, you need to convert the `.mhd` files to DICOM format to make them compatible with the MONAI pipeline. To do this, execute the following command:

```bash
python convert_image.py
```

This will run the `convert_image.py` script, which will convert all `.mhd` files in the specified folder to DICOM format.

---

## 🧠 Pretrained Model: Lung Nodule Detection

We use the MONAI Model Zoo’s pretrained model for lung nodule detection.

### Download the Pretrained Model

Instead of cloning a repository, download the pretrained model directly from GitHub. Access the model at the following URL, download `model.pt`, and place it in your project’s directory (e.g., in a folder like `/models`):

🔗 **Model Download Link**:  
[https://github.com/Project-MONAI/model-zoo](https://github.com/Project-MONAI/model-zoo)

Once downloaded, copy the `model.pt` file to the root directory of your project.

---

## 🔄 Full Pipeline Execution

### Step 1: Run the Application in Docker

Before running the full pipeline, make sure to start the application by running `app.py` inside the `lung_nodule` Docker container. This will allow you to process images through the pipeline.

In the terminal, run:

```bash
docker exec -it lung_nodule python app.py
```

### Step 2: Upload Images to Docker

To upload images to Docker, use the following `curl.exe` command to send the images to the Docker container:

```bash
curl.exe -X POST -F "file=@/path/to/image.dcm" http://localhost:5000/upload
```

Replace `/path/to/image.dcm` with the actual path to the DICOM image you want to upload.

### Step 3: Upload Images to Orthanc

Next, execute `orthanc_client.py` inside the `lung_nodule` Docker container to upload the images to Orthanc:

```bash
docker exec -it lung_nodule python orthanc_client.py
```

This will ensure that the images are transferred to Orthanc for further processing.

### Step 4: Run the Full Pipeline

Finally, execute the pipeline in Docker to process the images:

```bash
docker exec -it lung_nodule python pipeline.py
```

This will complete the full cycle of downloading, processing, and re-uploading the images.

### Step 5: View Processed Images in Orthanc

To visualize the processed images, access Orthanc at:

```bash
http://orthanc:8042/instances
```

You can view all the DICOM images that have been processed and uploaded to Orthanc.

---

## 🚀 Workflow Summary

This pipeline allows you to:

- Download DICOM images from Orthanc
- Modify and upload them to MONAI Deploy
- Perform inference using a pretrained lung nodule detection model
- Re-upload the processed images back to Orthanc

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---


