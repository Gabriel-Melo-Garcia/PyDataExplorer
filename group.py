from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QTextEdit, QComboBox, QPushButton
from PyQt6.QtGui import QFont
import pandas as pd

class GroupByDialog(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Group By Dialog")
        main_layout = QVBoxLayout()
        form_layout = QFormLayout()
        
        self.txt_widget = QTextEdit()
        self.txt_widget.setReadOnly(True)
        
        font = QFont()
        font.setPointSize(12)
        self.txt_widget.setFont(font)
        
        self.cb_col_to_group = QComboBox()
        self.cb_col_target = QComboBox()
        self.cb_method = QComboBox()
        
        self.cb_col_to_group.addItems(self.data.columns)
        self.cb_col_target.addItems(self.data.columns)
        self.cb_method.addItems(['mean', 'sum'])
        
        btn_show = QPushButton('Show')
        btn_show.clicked.connect(self.show_group)
        
        form_layout.addRow('Column to Group', self.cb_col_to_group)
        form_layout.addRow('Column Target', self.cb_col_target)
        form_layout.addRow('Method', self.cb_method)
        
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.txt_widget)
        main_layout.addWidget(btn_show)
        
        self.setLayout(main_layout)
    
    def show_group(self):
        try:
            txt_col_1 = self.cb_col_to_group.currentText()
            txt_col_2 = self.cb_col_target.currentText()
            txt_method = self.cb_method.currentText()

            if txt_method == 'mean':
                result = self.data.groupby(txt_col_1)[txt_col_2].mean()
            else:
                result = self.data.groupby(txt_col_1)[txt_col_2].sum()

            group_string = [f'{txt_method} {txt_col_2} grouped by {txt_col_1}']
            group_string.extend(f"{index}:  {value:.2f}" for index, value in result.items())

            self.txt_widget.setPlainText("\n".join(group_string))
        except Exception as e:
            self.txt_widget.setPlainText(f'Error: {e}')