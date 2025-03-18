from PyQt6.QtCore import QThread, pyqtSignal
import joblib
from PyQt6.QtWidgets import QFileDialog

class ClassificationWorker(QThread):
    finished = pyqtSignal(bool, str, dict)
    progress = pyqtSignal(str)
  
    def __init__(self, model, features, target, model_name):
        super().__init__()
        self.model = model
        self.features = features
        self.target = target
        self.model_name = model_name
  
    def run(self):
        success, message, results = self.model.train_classification_models(self.features, self.target, self.model_name)
        self.finished.emit(success, message, results)