# 🫁 Lung Nodule Detection with MONAI Deploy

This project implements a full pipeline for working with medical images in DICOM format, using **MONAI Deploy** and a pretrained model for lung nodule detection on CT scans.

---

## 📦 Project Setup

To use this repository, you need to set up a Python virtual environment with MONAI and all required libraries.

### 1. Activate the MONAI Environment

In your terminal:

```bash
.\your_folder_name\Scripts\python.exe
```

Then activate the environment:

- On **Command Prompt or PowerShell**:

```bash
.\your_folder_name\Scripts\activate
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

After downloading, convert the `.mhd` files to DICOM format to make them compatible with the MONAI pipeline.

---

## 🧠 Pretrained Model: Lung Nodule Detection

We use MONAI Model Zoo’s pretrained model for lung nodule detection.

### Clone the Repository

```bash
git clone https://github.com/Project-MONAI/model-zoo.git
```

### Navigate to the Model Directory

```bash
cd model-zoo/models/lung_nodule_ct_detection
```

### Copy the Pretrained Model to Your Project

```bash
cp model.pt /path/to/your/project
```

Make sure `model.pt` is located at the root of your project directory.

---


## 🚀 Workflow Summary

This pipeline allows you to:

- Download DICOM images from Orthanc
- Modify and upload them to MONAI Deploy
- Perform inference using a pretrained lung nodule detection model
- Re-upload the processed images back to Orthanc

---




