from PyQt6.QtCore import QThread, pyqtSignal
import joblib
from PyQt6.QtWidgets import QFileDialog


class ClassificationWorker(QThread):
    finished = pyqtSignal(bool, str)
    progress = pyqtSignal(str)
  
    def __init__(self, classification_model, data, features, target, model_name):
        super().__init__()
        self.data = data
        self.classification_model = classification_model
        self.features = features
        self.target = target
        self.model_name = model_name
  
    def run(self):
        success, message = self.classification_model.train_model(self.data, self.features, self.target, self.model_name)
        self.finished.emit(success, message)