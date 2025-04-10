from orthanc.orthanc_client import OrthancClient

class DownloadFromOrthanc:
    def __init__(self): 
        self.orthanc_client = OrthancClient()

    def run(self):
        print("⬇ Ejecutando DownloadFromOrthanc...")
        self.orthanc_client.download_first_dicom()


if __name__ == "__main__":  
    downloader = DownloadFromOrthanc()
    downloader.run()