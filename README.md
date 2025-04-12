
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

## 📝 Run the Full Pipeline

To execute the entire pipeline, follow these steps:

### 1. Copy Files to the Docker Container

First, you need to copy the necessary files into the `lung_nodule` Docker container. Use the following command to do this:

```bash
docker cp /path/to/your/project lung_nodule:/path/in/container
```

Replace `/path/to/your/project` with the actual path to your project folder and `/path/in/container` with the destination folder in the container.

### 2. Execute the Pipeline Inside the Docker Container

Once the files are copied, you can execute the `pipeline.py` script inside the Docker container to run the entire pipeline. Use the following command:

```bash
docker exec -it lung_nodule python /path/in/container/pipeline.py
```

This will execute the pipeline, processing the DICOM images, running inference, and uploading the processed images back to Orthanc.

---

## 👁 Visualize Processed Images in Orthanc

To view the processed images, open your browser and navigate to the following URL:

```
http://orthanc:8042/instances
```

This will display all the images stored in Orthanc, including the ones processed by the pipeline.

---

## 🚀 Workflow Summary

This pipeline allows you to:

- Download DICOM images from Orthanc
- Modify and upload them to MONAI Deploy
- Perform inference using a pretrained lung nodule detection model
- Re-upload the processed images back to Orthanc

---




