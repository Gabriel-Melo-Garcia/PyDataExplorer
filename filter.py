from PyQt6.QtWidgets import (QDialog, QFormLayout, QComboBox,
QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
QListWidget, QCheckBox,QWidget,QListWidgetItem)
import pandas as pd

class FilterDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.data = data
        self.filtered_data = data.copy()
        
        self.setWindowTitle("Filter")
        self.layout = QVBoxLayout()

        # Dropdowns for selecting columns and actions
        self.cb_column = QComboBox()
        self.cb_column.addItems(self.data.columns)
        self.cb_action = QComboBox()
        self.change_action()
        self.cb_column.currentIndexChanged.connect(self.change_action)

        self.txt_input_line = QLineEdit()
        self.txt_input_line.setPlaceholderText("Value")
        
        # Add Condition Button
        self.btn_add_condition = QPushButton("Add Condition")
        self.btn_add_condition.clicked.connect(self.add_condition)
        
        # Conditions List
        self.conditions_list = QListWidget()
        
        # Column Selection Button
        self.btn_select_columns = QPushButton("Select Columns")
        self.btn_select_columns.clicked.connect(self.select_columns)
        
        # Apply and Cancel Buttons
        self.btn_apply = QPushButton("Apply")
        self.btn_apply.clicked.connect(self.apply_filter)
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.clicked.connect(self.reject)
        
        # Layout Setup
        form_layout = QFormLayout()
        form_layout.addRow("Column", self.cb_column)
        form_layout.addRow("Action", self.cb_action)
        form_layout.addRow("Value", self.txt_input_line)
        form_layout.addRow(self.btn_add_condition)
        
        self.layout.addLayout(form_layout)
        self.layout.addWidget(QLabel("Conditions:"))
        self.layout.addWidget(self.conditions_list)
        self.layout.addWidget(self.btn_select_columns)
        
        # Buttons layout
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_apply)
        btn_layout.addWidget(self.btn_cancel)
        self.layout.addLayout(btn_layout)
        
        self.setLayout(self.layout)

        # Column selection dialog
        self.selected_columns = list(self.data.columns)
    
    def add_condition(self):
        column = self.cb_column.currentText()
        action = self.cb_action.currentText()
        value = self.txt_input_line.text()
        data_type = self.data[column].dtype
        if data_type == 'int64' or data_type == 'float64':
            try:
                value = float(value) if '.' in value else int(value)
            except ValueError:
                return
            condition_text = f"{column} {action} {value}"
        else:
            condition_text = f"{column} {action} '{value}'"
            
        list_item = QListWidgetItem(condition_text)  
        self.conditions_list.addItem(list_item)
    
        btn_remove = QPushButton("X")
        btn_remove.setFixedSize(20, 20)

        def remove_condition():
            self.conditions_list.takeItem(self.conditions_list.row(list_item))

        btn_remove.clicked.connect(remove_condition)

        # Criando um widget personalizado para armazenar o layout
        item_widget = QWidget()
        item_layout = QHBoxLayout()
        item_layout.addWidget(QLabel(condition_text))
        item_layout.addWidget(btn_remove)
        item_layout.setContentsMargins(0, 0, 0, 0)
        item_layout.setSpacing(5)
        item_widget.setLayout(item_layout)

        self.conditions_list.setItemWidget(list_item, item_widget)
    
    def select_columns(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Columns")
        layout = QVBoxLayout()
        checkboxes = []
        
        for col in self.data.columns:
            checkbox = QCheckBox(col)
            checkbox.setChecked(col in self.selected_columns)
            layout.addWidget(checkbox)
            checkboxes.append(checkbox)
        
        def save_selection():
            self.selected_columns = [cb.text() for cb in checkboxes if cb.isChecked()]
            dialog.accept()
        
        btn_save = QPushButton("Save")
        btn_save.clicked.connect(save_selection)
        layout.addWidget(btn_save)
        
        dialog.setLayout(layout)
        dialog.exec()
    
    def apply_filter(self):
        if self.conditions_list.count()>0:
            try:
                query_conditions = []
                for index in range(self.conditions_list.count()):
                    query_conditions.append(self.conditions_list.item(index).text())
                
                query_string = " and ".join(query_conditions)
                self.filtered_data = self.data.query(query_string)
                self.filtered_data = self.filtered_data[self.selected_columns]
                self.accept()
            except Exception as e:
                print(f"Error: {e}")
        else:
            try: 
                self.filtered_data = self.filtered_data[self.selected_columns]
                self.accept()
            except Exception as e:
                print(f"Error: {e}")
            
    def change_action(self):
                actions_list = ['==','!=','<','>','<=','>=']
                
                col_name = self.cb_column.currentText()
                data_type = self.data[col_name].dtype
                if data_type == 'int64' or data_type == 'float64':
                    self.cb_action.clear()
                    self.cb_action.addItems(actions_list)
                else:
                    self.cb_action.clear()
                    self.cb_action.addItems(['==','!='])
