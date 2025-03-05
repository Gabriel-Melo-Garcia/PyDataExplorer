from PyQt6.QtWidgets import QDialog, QFormLayout, QComboBox, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal

class ChangeTypeView(QDialog):
    apply_change_signal = pyqtSignal(str, str, str)  # column, new_type, true_value

    def __init__(self, column, parent=None):
        super().__init__(parent)
        self.column = column
        self.setWindowTitle(f"Change type of column {column}")
        self.setMinimumSize(300, 120)
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        self.cb_type = QComboBox()
        self.cb_type.addItems(["str", "int", "float", "bool", "date"])
        self.lb_bool = QLabel("True value:")
        self.cb_bool = QComboBox()
        self.lb_error = QLabel("")
        self.lb_error.setStyleSheet("color: red")
        self.lb_bool.setVisible(False)
        self.cb_bool.setVisible(False)

        self.cb_type.currentTextChanged.connect(self.update_bool_combo)

        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")
        save_button.clicked.connect(self.apply_change)
        cancel_button.clicked.connect(self.reject)

        layout.addRow("New type:", self.cb_type)
        layout.addRow(self.lb_bool, self.cb_bool)
        layout.addRow(self.lb_error)
        layout.addRow(save_button, cancel_button)
        self.setLayout(layout)

    def update_bool_combo(self):
        if self.cb_type.currentText() == "bool":
            self.lb_bool.setVisible(True)
            self.cb_bool.setVisible(True)
            # O Controller pode preencher os valores únicos aqui via método separado
        else:
            self.lb_bool.setVisible(False)
            self.cb_bool.setVisible(False)

    def apply_change(self):
        true_value = self.cb_bool.currentText() if self.cb_type.currentText() == "bool" else None
        self.apply_change_signal.emit(self.column, self.cb_type.currentText(), true_value)
        self.accept()

    def set_unique_values(self, values):
        if self.cb_type.currentText() == "bool":
            unique_vals = [str(v) for v in values]
            if len(unique_vals) > 2:
                self.lb_error.setText("Error: Column has more than 2 unique values")
                self.cb_bool.clear()
                self.cb_bool.setEnabled(False)
            else:
                self.cb_bool.clear()
                self.cb_bool.addItems(unique_vals)
                self.cb_bool.setEnabled(True)
                self.lb_error.clear()