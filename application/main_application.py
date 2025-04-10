from monai.deploy.core import Application, Fragment
from operators.upload_operator import UploadToMONAIOperator
from operators.inference_operator import InferenceOperator

class MainApplication:
    def __init__(self):
        self.app = Application()
        self.fragment = Fragment(self.app)
        self.upload_operator = UploadToMONAIOperator(self.fragment)
        self.inference_operator = InferenceOperator(self.fragment)

    def run(self):
        self.upload_operator.compute(None)
        self.inference_operator.compute(None)
