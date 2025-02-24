from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QWidget, QLineEdit,QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog,
    QDialog, QComboBox, QFormLayout, QPushButton,QTableWidget
)
from PyQt6.QtGui import QAction
from PyQt6.QtGui import QAction
import sys
import pandas as pd

class Main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = None
        self.filtered_data = None
        self.initui()
        
    def initui(self):
        
    # creating menu bar
        menubar = self.menuBar()
        self.change_type_menu = menubar.addMenu("Change Type")
        self.null_value_handling_menu = menubar.addMenu("Handle Null")
        
        #initiating the main widget and layouts
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        left_list_layout = QVBoxLayout()
        labels_layout = QVBoxLayout()        
        
        #btn add dataframe
        self.btn_add_dataframe = QPushButton("Add DataFrame")
        self.btn_add_dataframe.clicked.connect(self.add_data)
        #btn filter data
        self.btn_filter_data = QPushButton("filter")
        self.btn_filter_data.clicked.connect(self.filter_data)
        #btn clean filter
        self.btn_show_info = QPushButton("clean filter")
        self.btn_show_info.clicked.connect(self.show_info)
        

        self.table_widget = QTableWidget()
        
        self.lb_3 = QLabel("local da tabela")
        self.lb_4 = QLabel("label qualquer")
        
        
        left_list_layout.addWidget(self.btn_add_dataframe)
        left_list_layout.addWidget(self.btn_filter_data)
        left_list_layout.addWidget(self.btn_show_info)
        
        labels_layout.addWidget(self.table_widget,3)
        labels_layout.addWidget(self.lb_4,1)
        
        main_layout.addLayout(left_list_layout,1)
        main_layout.addLayout(labels_layout,3)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        # self.setGeometry(200,200,600,400)
        self.setMinimumSize(600,400)
        self.show()
        
    def add_data(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open CSV File", "./data", "Files (*.csv *.xlsx)")
        
        if file_path:
            if file_path.endswith(".csv"):
                self.data = pd.read_csv(file_path)
            else:
                self.data = pd.read_excel(file_path)
        
        self.lb_4.setText(f'O datafame foi adicionado')
        self.update_change_type_menu() 
        self.update_null_handling_menu()
        self.update_defaut_table()
        
    def show_info(self):
        if self.data is not None:
            self.update_defaut_table()
        else:
            self.table_widget.setRowCount(0)
            self.table_widget.setColumnCount(0)
            
    def update_defaut_table(self):
        if self.data is not None:
            self.table_widget.setRowCount(self.data.shape[0])
            self.table_widget.setColumnCount(self.data.shape[1])
            self.table_widget.setHorizontalHeaderLabels(self.data.columns)
            
            for row in range(self.data.shape[0]):
                for col in range(self.data.shape[1]):
                    item = QTableWidgetItem(str(self.data.iat[row, col]))
                    self.table_widget.setItem(row, col, item)
        else:
            self.table_widget.setRowCount(0)
            self.table_widget.setColumnCount(0)
            
    def update_filtered_table(self):
        if self.filtered_data is not None:
            self.table_widget.setRowCount(self.filtered_data.shape[0])
            self.table_widget.setColumnCount(self.filtered_data.shape[1])
            self.table_widget.setHorizontalHeaderLabels(self.filtered_data.columns)
            
            for row in range(self.filtered_data.shape[0]):
                for col in range(self.filtered_data.shape[1]):
                    item = QTableWidgetItem(str(self.filtered_data.iat[row, col]))
                    self.table_widget.setItem(row, col, item)
        else:
            self.table_widget.setRowCount(0)
            self.table_widget.setColumnCount(0)
            
    def update_change_type_menu(self):
        self.change_type_menu.clear()
        if self.data is not None:
            for column in self.data.columns:
                action = QAction(column, self)
                action.triggered.connect(self.change_type)
                self.change_type_menu.addAction(action)
        else:
            self.change_type_menu.addAction("Nenhum DataFrame carregado").setEnabled(False)
        
    def update_null_handling_menu(self):
        self.null_value_handling_menu.clear()
        if self.data is not None:
            for column in self.data.columns:
                action = QAction(column, self)
                action.triggered.connect(self.handle_null)
                self.null_value_handling_menu.addAction(action)
        else:
            self.null_value_handling_menu.addAction("Nenhum DataFrame carregado").setEnabled(False)
                  
    def change_type(self):
        column = self.sender()
        if self.data is not None and column:
            col_name = column.text()
            current_type = str(self.data[col_name].dtype)
            
            dialog = QDialog(self)
            dialog.setWindowTitle(f"change type of the column {col_name}")
            dialog.setMinimumSize(300, 100)
            layout = QFormLayout()
            
            type_combo = QComboBox()
            type_combo.addItems(["str", "int", "float", "bool"])
            type_combo.setCurrentText(current_type)
            
            save_button = QPushButton("save")
            cancel_button = QPushButton("Cancel")
            
            def apply_change():
                try:
                    new_type = type_combo.currentText()
                    self.data[col_name] = self.data[col_name].astype(new_type)
                    self.lb_4.setText(f"Coluna '{col_name}' convertida para {new_type}")
                    self.update_defaut_table()
                    dialog.accept()
                except Exception as e:
                    self.lb_4.setText(f"um erro ocorreu durante a mudança: {e}")
                    dialog.reject()
            
            save_button.clicked.connect(apply_change)
            cancel_button.clicked.connect(dialog.reject)
            
            layout.addRow("Novo tipo:", type_combo)
            layout.addRow(save_button, cancel_button)
            dialog.setLayout(layout)
            dialog.exec()
        else:
            self.lb_4.setText("Erro ao converter a coluna")
  
    def handle_null(self):
        column = self.sender()
        if self.data is not None and column:
            col_name = column.text()
            # current_type = str(self.data[col_name].dtype)
            
            dialog = QDialog(self)
            dialog.setWindowTitle(f"change type of the column {col_name}")
            dialog.setMinimumSize(300, 100)
            layout = QFormLayout()
            
            null_handle_combo = QComboBox()
            null_handle_combo.addItems(["fill whith mean value",
                                        "fill whith median value",
                                        "fill with 0",
                                        "delete null rows"
                                        ])
            save_button = QPushButton("save")
            cancel_button = QPushButton("Cancel")
            
            def apply_change():
                try:
                    cb_index = null_handle_combo.currentIndex()
                    if cb_index == 0:
                        self.data[col_name] = self.data[col_name].fillna(self.data[col_name].mean())
                    elif cb_index == 1:
                        self.data[col_name] = self.data[col_name].fillna(self.data[col_name].median())
                    elif cb_index == 2:
                        self.data[col_name] = self.data[col_name].fillna(0)
                    elif cb_index == 3:
                        self.data = self.data.dropna(subset=[col_name])
                    self.lb_4.setText(f"Coluna '{col_name}' tratada")
                    self.update_defaut_table()
                    dialog.accept()
                except Exception as e:
                    self.lb_4.setText(f"Um erro ocorreu durante a mudança: {e}")
                    dialog.reject()
            
            save_button.clicked.connect(apply_change)
            cancel_button.clicked.connect(dialog.reject)
            
            layout.addRow("Novo tipo:", null_handle_combo)
            layout.addRow(save_button, cancel_button)
            dialog.setLayout(layout)
            dialog.exec()
        else:
            self.lb_4.setText("Erro ao converter a coluna")
    
    def filter_data(self):
        if self.data is not None:
            
            actions_list = ['==','!=','<','>','<=','>=']
            
            def change_action():
                
                col_name = cb_column.currentText()
                data_type = self.data[col_name].dtype
                if data_type == 'int64' or data_type == 'float64':
                    cb_action.clear()
                    cb_action.addItems(actions_list)
                else:
                    cb_action.clear()
                    cb_action.addItems(['==','!='])
                
            
            dialog = QDialog(self)
            dialog.setWindowTitle("filter")
            
            layout = QFormLayout()

            cb_column = QComboBox()
            cb_column.addItems(self.data.columns)
            cb_action = QComboBox()
            change_action()
            
            cb_column.currentIndexChanged.connect(change_action)
                   
            txt_input_line = QLineEdit()
            txt_input_line.setPlaceholderText("value")
            save_button = QPushButton("save")
            cancel_button = QPushButton("Cancel")
            
            def apply_filter():
                try:
                    col_name = cb_column.currentText()
                    action_txt = cb_action.currentText()
                    value_txt = txt_input_line.text()
                    
                    data_type = self.data[col_name].dtype
                    
                    if data_type == 'int64' or data_type == 'float64':
                        value = eval(value_txt)
                        self.filtered_data = self.data.query(f"{col_name} {action_txt} {value}")
                    else:
                        self.filtered_data = self.data.query(f"{col_name} {action_txt} '{value_txt}'")
                    
                    # print(self.filtered_data.head())
                    self.update_filtered_table()
                    dialog.accept()
                    
                except Exception as e:
                    self.lb_4.setText(f"Error: {e}")
                    dialog.reject()
            
            save_button.clicked.connect(apply_filter)
            cancel_button.clicked.connect(dialog.reject)
            
            layout.addRow("column",cb_column)
            layout.addRow("action",cb_action)
            layout.addRow(txt_input_line)
            layout.addRow(save_button, cancel_button)
            dialog.setLayout(layout)
            dialog.exec()
        else:
            self.lb_4.setText("No dataframe loaded")
             
    
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    window = Main_window()
    sys.exit(app.exec())