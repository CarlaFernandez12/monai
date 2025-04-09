from monai.deploy.core import Application, Fragment
from upload_operator import UploadToMONAIOperator

class MainApplication:
    def __init__(self):
        self.app = Application()
        self.fragment = Fragment(self.app)
        self.operator = UploadToMONAIOperator(self.fragment)

    def run(self):
        self.operator.compute(None)