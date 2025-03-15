from PyQt6.QtCore import QThread, pyqtSignal
import joblib
from PyQt6.QtWidgets import QFileDialog

class ChangeTypeWorker(QThread):
    finished = pyqtSignal(bool, str)
    progress = pyqtSignal(str)

    def __init__(self, model, column, new_type, true_value):
        super().__init__()
        self.model = model
        self.column = column
        self.new_type = new_type
        self.true_value = true_value

    def run(self):
        success, message = self.model.change_type(self.column, self.new_type, self.true_value)
        self.finished.emit(success, message)