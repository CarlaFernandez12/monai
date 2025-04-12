import os

UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "uploads"))
os.makedirs(UPLOAD_FOLDER,exist_ok=True) 