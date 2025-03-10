import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QApplication, QTabWidget,
    QVBoxLayout, QComboBox, QLineEdit, QPushButton, QLabel
)
from PyQt6.QtCore import pyqtSignal

class MapValuesView(QMainWindow):
    create_column_signal = pyqtSignal(str)
    replace_values_signal = pyqtSignal(str,str,str)
    update_values_by_condition_signal = pyqtSignal(str,str,str,str,str)
    
    def __init__(self,columns):
        super().__init__()
        self.setMinimumSize(400, 400)
        self.setWindowTitle("DataFrame Editor")
        self.columns = columns
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        # Tab setup
        self.tabs = QTabWidget()
        self.tab_create_column = QWidget()
        self.tab_replace_values = QWidget()
        self.tab_update_by_condition = QWidget()

        self.tabs.addTab(self.tab_create_column, "Create Column")
        self.tabs.addTab(self.tab_replace_values, "Replace Values")
        self.tabs.addTab(self.tab_update_by_condition, "Update by Condition")
        
        # -----------------------------
        # tab create column
        self.layout_create_column = QVBoxLayout(self.tab_create_column)
        
        # Input field for column name
        self.layout_create_column.addWidget(QLabel("New column name:"))
        self.create_column_name = QLineEdit()
        self.layout_create_column.addWidget(self.create_column_name)
        
        # Button to execute
        self.btn_create = QPushButton("Create Column")
        self.btn_create.clicked.connect(self.execute_create_column)
        self.layout_create_column.addWidget(self.btn_create)
        self.layout_create_column.addStretch()
    
        # -----------------------------
        # tab replace values
        
        self.layout_replace_values = QVBoxLayout(self.tab_replace_values)
        
        # Column selection
        self.layout_replace_values.addWidget(QLabel("Select column:"))
        self.cb_replace_column = QComboBox()
        # self.cb_replace_column.addItems(self.columns)
        self.layout_replace_values.addWidget(self.cb_replace_column)
        
        # Old value
        self.layout_replace_values.addWidget(QLabel("Old value:"))
        self.replace_old_value = QLineEdit()
        self.layout_replace_values.addWidget(self.replace_old_value)
        
        # New value
        self.layout_replace_values.addWidget(QLabel("New value:"))
        self.replace_new_value = QLineEdit()
        self.layout_replace_values.addWidget(self.replace_new_value)
        
        # Button to execute
        self.btn_replace = QPushButton("Replace")
        self.btn_replace.clicked.connect(self.replace_values)
        self.layout_replace_values.addWidget(self.btn_replace)
        self.layout_replace_values.addStretch()
        
        # -----------------------------
        # tab update by condition
        
        self.layout_update_by_condition = QVBoxLayout(self.tab_update_by_condition)
        
        # Target column
        self.layout_update_by_condition.addWidget(QLabel("Target column:"))
        self.cb_target_column = QComboBox()
        # self.cb_target_column.addItems(self.columns)
        self.layout_update_by_condition.addWidget(self.cb_target_column)
        
        # New value
        self.layout_update_by_condition.addWidget(QLabel("New value:"))
        self.target_value = QLineEdit()
        self.layout_update_by_condition.addWidget(self.target_value)
        
        # Condition column
        self.layout_update_by_condition.addWidget(QLabel("Condition column:"))
        self.cb_condition_column = QComboBox()
        # self.cb_condition_column.addItems(self.columns)
        self.layout_update_by_condition.addWidget(self.cb_condition_column)
        
        # Operator
        self.layout_update_by_condition.addWidget(QLabel("Operator:"))
        self.cb_operator = QComboBox()
        self.cb_operator.addItems(['<', '>', '<=', '>=', '==', '!='])
        self.layout_update_by_condition.addWidget(self.cb_operator)
        
        # Condition value
        self.layout_update_by_condition.addWidget(QLabel("Condition value:"))
        self.condition_value = QLineEdit()
        self.layout_update_by_condition.addWidget(self.condition_value)
        
        # Button to execute
        self.btn_update = QPushButton("Update")
        self.btn_update.clicked.connect(self.update_values_by_condition)
        self.layout_update_by_condition.addWidget(self.btn_update)
        self.layout_update_by_condition.addStretch()
        
        self.update_columns_cb(self.columns)
        
        self.main_layout.addWidget(self.tabs)

    def execute_create_column(self):
        
        name = self.create_column_name.text()
        if name:
            self.create_column_signal.emit(name)

    def replace_values(self):
        column = self.cb_replace_column.currentText()
        old_value = self.replace_old_value.text()
        new_value = self.replace_new_value.text()
        self.replace_values_signal.emit(column,old_value,new_value)

    def update_values_by_condition(self):
        
        condition_column = self.cb_condition_column.currentText()
        target_column = self.cb_target_column.currentText()
        operator = self.cb_operator.currentText()
        condition_value = self.condition_value.text()
        new_value = self.target_value.text()
        if condition_value == '':
            print('negado condição')
        elif new_value == '':
            print('negado novo valor')
        else:
            self.update_values_by_condition_signal.emit(
                condition_column,target_column,operator,
                condition_value,new_value
                )

    def update_columns_cb(self, columns):
        
        self.cb_condition_column.clear()
        self.cb_replace_column.clear()
        self.cb_target_column.clear()
        
        if columns:
            self.cb_condition_column.addItems(columns)
            self.cb_replace_column.addItems(columns)
            self.cb_target_column.addItems(columns)