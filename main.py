from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QWidget, QLineEdit,QTableWidgetItem,QDockWidget,
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog,QTextEdit,
    QDialog, QComboBox, QFormLayout, QPushButton,QTableWidget
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
import io
import sys
import pandas as pd
from filter import FilterDialog
from graph_view import GraphView

class Main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = None
        self.filtered_data = None
        self.graph_window = None  
        self.initui()
        self.initDrawer()
        
    def initui(self):
        
    # creating menu bar
        menubar = self.menuBar()
        self.change_type_menu = menubar.addMenu("Change Type")
        self.null_value_handling_menu = menubar.addMenu("Handle Null")
        
        #initiating the main widget and layouts
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        left_btn_list_layout = QVBoxLayout()
        table_layout = QVBoxLayout()        
        
        #btn add dataframe
        self.btn_add_dataframe = QPushButton("Add DataFrame")
        self.btn_add_dataframe.clicked.connect(self.add_data)
        #btn filter data
        self.btn_filter_data = QPushButton("filter")
        self.btn_filter_data.clicked.connect(self.filter_data)
        #btn clean filter
        self.btn_clean_filter = QPushButton("clean filter")
        self.btn_clean_filter.clicked.connect(self.update_defaut_table)
        #btn show details
        self.btn_show_details = QPushButton("Mostrar Detalhes")
        self.btn_show_details.clicked.connect(self.toggleDrawer)
        #btn open graph
        self.btn_open_graph = QPushButton("Graph")
        self.btn_open_graph.clicked.connect(self.open_graph_window)
        
        self.table_widget = QTableWidget()
    
        self.lb_4 = QLabel("label qualquer")
        
        left_btn_list_layout.addWidget(self.btn_add_dataframe)
        left_btn_list_layout.addWidget(self.btn_filter_data)
        left_btn_list_layout.addWidget(self.btn_show_details)
        left_btn_list_layout.addWidget(self.btn_clean_filter)
        left_btn_list_layout.addWidget(self.btn_open_graph)
        
        table_layout.addWidget(self.table_widget,4)
        table_layout.addWidget(self.lb_4,1)
        
        main_layout.addLayout(left_btn_list_layout,1)
        main_layout.addLayout(table_layout,3)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        # self.setGeometry(200,200,600,400)
        self.setMinimumSize(850,550)
        self.show()
        
    def add_data(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open csv/xlsx File", "./data", "Files (*.csv *.xlsx)")
        
        if file_path:
            if file_path.endswith(".csv"):  
                self.data = pd.read_csv(file_path)
            else:
                self.data = pd.read_excel(file_path)
        
        self.lb_4.setText(f'The data was loaded with {self.data.shape[0]} rows and {self.data.shape[1]} columns')
        self.update_change_type_menu() 
        self.update_null_handling_menu()
        self.update_defaut_table()
            
    def update_defaut_table(self):
        if self.data is not None:
            self.table_widget.setRowCount(self.data.shape[0])
            self.table_widget.setColumnCount(self.data.shape[1])
            self.table_widget.setHorizontalHeaderLabels(self.data.columns)
            
            for row in range(self.data.shape[0]):
                for col in range(self.data.shape[1]):
                    item = QTableWidgetItem(str(self.data.iat[row, col]))
                    self.table_widget.setItem(row, col, item)
            self.lb_4.setText(f'The dataframe have {self.data.shape[0]} rows and {self.data.shape[1]} columns')
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
            self.change_type_menu.addAction("No Dataframe Loaded").setEnabled(False)
        
    def update_null_handling_menu(self):
        self.null_value_handling_menu.clear()
        if self.data is not None:
            for column in self.data.columns:
                action = QAction(column, self)
                action.triggered.connect(self.handle_null)
                self.null_value_handling_menu.addAction(action)
        else:
            self.null_value_handling_menu.addAction("No Dataframe Loaded").setEnabled(False)
                  
    def change_type(self):
        column = self.sender()
        if self.data is not None and column:
            col_name = column.text()
            current_type = str(self.data[col_name].dtype)

            dialog = QDialog(self)
            dialog.setWindowTitle(f"Change type of column {col_name}")
            dialog.setMinimumSize(300, 120)
            layout = QFormLayout()

            type_combo = QComboBox()
            type_combo.addItems(["str", "int", "float", "bool"])
            type_combo.setCurrentText(current_type)

            bool_combo = QComboBox()
            bool_combo.setVisible(False)

            error_label = QLabel("")
            error_label.setStyleSheet("color: red")

            def show_bool_combo():
                if type_combo.currentText() == "bool":
                    unique_values = self.data[col_name].dropna().unique()

                    if len(unique_values) > 2:
                        error_label.setText("Erro: A coluna tem mais de 2 valores únicos")
                        bool_combo.setVisible(False)
                        return

                    bool_combo.clear()
                    bool_combo.addItems([str(v) for v in unique_values]) 
                    bool_combo.setVisible(True)
                    error_label.clear()
                else:   
                    bool_combo.setVisible(False)
                    error_label.clear()

            type_combo.currentTextChanged.connect(show_bool_combo)

            save_button = QPushButton("Save")
            cancel_button = QPushButton("Cancel")

            def apply_change():
                try:
                    new_type = type_combo.currentText()

                    if new_type == "bool":
                        unique_values = self.data[col_name].dropna().unique()
                        if len(unique_values) != 2:
                            raise ValueError("Coluna não pode ser convertida para booleano.")

                        true_value = bool_combo.currentText()
                        self.data[col_name] = self.data[col_name].map(lambda x: x == true_value)

                    else:
                        self.data[col_name] = self.data[col_name].astype(new_type)

                    self.lb_4.setText(f"Coluna '{col_name}' convertida para {new_type}")
                    self.update_defaut_table()
                    dialog.accept()

                except Exception as e:
                    error_label.setText(f"Erro: {e}")

            save_button.clicked.connect(apply_change)
            cancel_button.clicked.connect(dialog.reject)

            layout.addRow("Novo tipo:", type_combo)
            layout.addRow("True value:", bool_combo)
            layout.addRow(error_label)
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
            dialog = FilterDialog(self, self.data)
            if dialog.exec():
                self.filtered_data = dialog.filtered_data
                self.update_filtered_table()   
                self.lb_4.setText(f'The data filtered have {self.filtered_data.shape[0]} rows and {self.filtered_data.shape[1]} columns') 
        else:
            self.lb_4.setText("No dataframe loaded")
             
    def initDrawer(self):

        self.drawer = QDockWidget("Details", self)
        self.drawer.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        
        self.drawer_text = QTextEdit()
        self.drawer_text.setReadOnly(True)
        self.drawer.setWidget(self.drawer_text)
        
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.drawer)
        self.drawer.hide()  # Oculta o drawer inicialmente

    def toggleDrawer(self):

        if self.drawer.isVisible():
            self.drawer.hide()
        else:
            self.updateDrawerInfo()
            self.drawer.show()

    def updateDrawerInfo(self):
        if self.data is not None:
            info_text = []

            buffer = io.StringIO()
            sys.stdout = buffer  
            self.data.info(verbose=True)
            sys.stdout = sys.__stdout__ 
            info_output = buffer.getvalue().split("\n") 

            filtered_info = []
            start_collecting = False  

            for line in info_output:
                if "---" in line:  
                    start_collecting = True
                if start_collecting:  
                    filtered_info.append(line)

            info_text.append("📌 DataFrame Info:\n")
            info_text.append("\n".join(filtered_info))

            info_text.append("\n Null Values:\n")
            info_text.append(str(self.data.isna().sum()))

            info_text.append("\n Duplicated Values:\n")
            info_text.append(str(self.data.duplicated().sum()))

            self.drawer_text.setPlainText("\n".join(info_text))
        else:
            self.drawer_text.setPlainText("No Dataframe Loaded")
            
    def open_graph_window(self):
       
        if self.data is not None:
            self.graph_window = GraphView(self, self.data)  
            self.graph_window.show()
        else:
            self.lb_4.setText("No data loaded")
    
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    window = Main_window()
    sys.exit(app.exec())
    