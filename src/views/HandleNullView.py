from PyQt6.QtWidgets import QDialog, QFormLayout, QComboBox, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal

class HandleNullView(QDialog):
    apply_null_handling_signal = pyqtSignal(str, str, str)  # column, method, interpolate_method

    def __init__(self, column, parent=None):
        super().__init__(parent)
        self.column = column
        self.setWindowTitle(f"Handle nulls in {column}")
        self.setMinimumSize(300, 120)
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        self.null_handle_combo = QComboBox()
        self.null_handle_combo.addItems(["mean", "median", "zero", "drop", "interpolate"])
        self.lb_interpolate = QLabel("Interpolate Method:")
        self.cb_interpolate = QComboBox()
        self.cb_interpolate.addItems(['linear', 'time', 'pad', 'nearest', 'zero', 'slinear', 'quadratic', 'cubic'])
        self.lb_interpolate.setVisible(False)
        self.cb_interpolate.setVisible(False)

        self.null_handle_combo.currentTextChanged.connect(self.update_interpolate_combo)

        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")
        save_button.clicked.connect(self.apply_change)
        cancel_button.clicked.connect(self.reject)

        layout.addRow("Method:", self.null_handle_combo)
        layout.addRow(self.lb_interpolate, self.cb_interpolate)
        layout.addRow(save_button, cancel_button)
        self.setLayout(layout)

    def update_interpolate_combo(self):
        self.lb_interpolate.setVisible(self.null_handle_combo.currentText() == "interpolate")
        self.cb_interpolate.setVisible(self.null_handle_combo.currentText() == "interpolate")

    def apply_change(self):
        interpolate_method = self.cb_interpolate.currentText() if self.null_handle_combo.currentText() == "interpolate" else None
        self.apply_null_handling_signal.emit(self.column, self.null_handle_combo.currentText(), interpolate_method)
        self.accept()