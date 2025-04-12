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

After downloading, convert the `.mhd` files to DICOM format by running the following command:

```bash
python convert_image.py
```

🗂️ The converted DICOM files will be saved in the `/dicom` folder.

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

## 🚀 Build and Start Containers

Before executing the full pipeline, you need to build and start the required Docker containers.

### Create Docker Network

First, create a Docker network so all containers can communicate:

```bash
docker network create lung_net
```

### 1. **Lung Nodule Container**

The **Lung Nodule** container is built from the `Dockerfile` provided in the project.

- Build the container:

```bash
docker build -t lung_nodule -f Dockerfile .
```

- Start the container in the created network:

```bash
docker run -d --name lung_nodule --network lung_net lung_nodule
```

### 2. **Orthanc Container**

The **Orthanc** container is built from the pre-built image `jodogne/orthanc`.

- Pull the Orthanc image:

```bash
docker pull jodogne/orthanc
```

- Run the Orthanc container in the created network:

```bash
docker run -d --name orthanc --network lung_net -p 8042:8042 jodogne/orthanc
```

### 3. **MONAI Deploy Container**

The **MONAI Deploy** container is based on the default MONAI Deploy image.

- Pull the MONAI Deploy image:

```bash
docker pull monai/monai-deploy
```

- Run the MONAI Deploy container in the created network:

```bash
docker run -d --name monai_deploy --network lung_net monai/monai-deploy
```

---

## 🏃‍♂️ Run Full Pipeline

Once the containers are up and running, follow these steps to execute the full pipeline.

### 1. **Upload Images to Docker Container**

Before running the full pipeline, you need to upload images to the `lung_nodule` container. This can be done using `curl.exe`:

```bash
curl -X POST -F "file=@uploads/image.dcm" http://localhost:5000/upload
```

🗂️ The images to be uploaded should be stored in the `/uploads` folder.

### 2. **Run `app.py` in Docker Lung Nodule**

Run the `app.py` script inside the **Lung Nodule** Docker container to start the image processing pipeline.

```bash
docker exec -it lung_nodule python app.py
```

### 3. **Execute `orthanc_client.py` to Upload Images to Orthanc**

Run `orthanc_client.py` inside the **Lung Nodule** container to upload processed images to Orthanc:

```bash
docker exec -it lung_nodule python orthanc_client.py
```

### 4. **Run the Full Pipeline**

Once the images are uploaded to Orthanc and processed by MONAI, you can execute the full pipeline:

```bash
docker exec -it lung_nodule python pipeline.py
```

🗂️ The images downloaded from Orthanc will be saved in the `/downloads` folder.  
🗂️ The images processed by MONAI will be saved in the `/infered` folder.

---

## 🔍 View Processed Images

After executing the full pipeline, you can view the processed images in Orthanc by navigating to the following URL in your browser:

[http://localhost:8042/instances](http://localhost:8042/instances)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.