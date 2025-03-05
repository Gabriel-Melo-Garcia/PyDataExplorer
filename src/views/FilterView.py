from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QComboBox, QLineEdit, QPushButton, QVBoxLayout, 
    QHBoxLayout, QLabel, QListWidget, QCheckBox, QWidget, QListWidgetItem
)
from PyQt6.QtCore import pyqtSignal

class FilterView(QDialog):
    add_condition_signal = pyqtSignal(str, str, str) 
    apply_filter_signal = pyqtSignal(list, list)     
    select_columns_signal = pyqtSignal()
    column_changed_signal = pyqtSignal(str)

    def __init__(self, columns, parent=None):
        super().__init__(parent)
        self.columns = columns
        self.selected_columns = columns.copy()
        self.conditions = []
        self.setWindowTitle("Filter")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Dropdowns para colunas e ações
        self.cb_column = QComboBox()
        self.cb_column.addItems(self.columns)
        self.cb_action = QComboBox()
        self.update_actions()
        self.cb_column.currentIndexChanged.connect(lambda: self.column_changed_signal.emit(self.cb_column.currentText()))

        self.txt_input_line = QLineEdit()
        self.txt_input_line.setPlaceholderText("Value")

        # Botão para adicionar condição
        self.btn_add_condition = QPushButton("Add Condition")
        self.btn_add_condition.clicked.connect(self.add_condition)

        # Lista de condições
        self.conditions_list = QListWidget()

        # Botão para selecionar colunas
        self.btn_select_columns = QPushButton("Select Columns")
        self.btn_select_columns.clicked.connect(self.select_columns_signal.emit)

        # Botões Aplicar e Cancelar
        self.btn_apply = QPushButton("Apply")
        self.btn_apply.clicked.connect(self.apply_filter)
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.clicked.connect(self.reject)

        # Montar layout
        form_layout = QFormLayout()
        form_layout.addRow("Column", self.cb_column)
        form_layout.addRow("Action", self.cb_action)
        form_layout.addRow("Value", self.txt_input_line)
        form_layout.addRow(self.btn_add_condition)

        layout.addLayout(form_layout)
        layout.addWidget(QLabel("Conditions:"))
        layout.addWidget(self.conditions_list)
        layout.addWidget(self.btn_select_columns)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_apply)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def update_actions(self):
        # O Controller atualizará as ações com base no tipo da coluna
        self.cb_action.clear()
        # Ações padrão antes de o Controller preencher
        self.cb_action.addItems(['==', '!='])

    def set_action_items(self, actions):
        self.cb_action.clear()
        self.cb_action.addItems(actions)

    def add_condition(self):
        column = self.cb_column.currentText()
        action = self.cb_action.currentText()
        value = self.txt_input_line.text()
        self.add_condition_signal.emit(column, action, value)

    def add_condition_to_list(self, condition_text):
        list_item = QListWidgetItem(condition_text)
        self.conditions_list.addItem(list_item)
        self.conditions.append(condition_text)

        btn_remove = QPushButton("X")
        btn_remove.setFixedSize(20, 20)
        btn_remove.clicked.connect(lambda: self.remove_condition(list_item))

        item_widget = QWidget()
        item_layout = QHBoxLayout()
        item_layout.addWidget(QLabel(condition_text))
        item_layout.addWidget(btn_remove)
        item_layout.setContentsMargins(0, 0, 0, 0)
        item_layout.setSpacing(5)
        item_widget.setLayout(item_layout)

        self.conditions_list.setItemWidget(list_item, item_widget)

    def remove_condition(self, item):
        index = self.conditions_list.row(item)
        self.conditions_list.takeItem(index)
        self.conditions.pop(index)

    def apply_filter(self):
        self.apply_filter_signal.emit(self.conditions, self.selected_columns)
        self.accept()

    def show_column_selection(self, columns, selected_columns):
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Columns")
        layout = QVBoxLayout()
        checkboxes = []

        for col in columns:
            checkbox = QCheckBox(col)
            checkbox.setChecked(col in selected_columns)
            layout.addWidget(checkbox)
            checkboxes.append(checkbox)

        btn_save = QPushButton("Save")
        btn_save.clicked.connect(lambda: self.update_selected_columns([cb.text() for cb in checkboxes if cb.isChecked()], dialog))
        layout.addWidget(btn_save)

        dialog.setLayout(layout)
        dialog.exec()

    def update_selected_columns(self, selected_columns, dialog):
        self.selected_columns = selected_columns
        dialog.accept()