from monai.deploy.core import Application, env
from inference import InferenceOperator

@env(pip_packages=["monai", "pydicom", "pynetdicom", "torch"])
class MyMonaiApp(Application):
    def compose(self):
        self.add_operator(InferenceOperator())
